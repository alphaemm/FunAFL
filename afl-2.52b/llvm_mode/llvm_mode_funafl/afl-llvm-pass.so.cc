/*
   american fuzzy lop - LLVM-mode instrumentation pass
   ---------------------------------------------------

   Written by Laszlo Szekeres <lszekeres@google.com> and
              Michal Zalewski <lcamtuf@google.com>

   LLVM integration design comes from Laszlo Szekeres. C bits copied-and-pasted
   from afl-as.c are Michal's fault.

   Copyright 2015, 2016 Google Inc. All rights reserved.

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at:

     http://www.apache.org/licenses/LICENSE-2.0

   This library is plugged into LLVM when invoking clang through afl-clang-fast.
   It tells the compiler to add code roughly equivalent to the bits discussed
   in ../afl-as.h.

 */

#define AFL_LLVM_PASS

#include "../config.h"
#include "../debug.h"

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

#include "llvm/ADT/Statistic.h"
#include "llvm/IR/IRBuilder.h"
#include "llvm/IR/LegacyPassManager.h"
#include "llvm/IR/Module.h"
#include "llvm/Support/Debug.h"
#include "llvm/Transforms/IPO/PassManagerBuilder.h"
#include "llvm/Transforms/Utils/BasicBlockUtils.h"

using namespace llvm;

namespace {

  class AFLCoverage : public ModulePass {

    public:

      static char ID;
      AFLCoverage() : ModulePass(ID) { }

      bool runOnModule(Module &M) override;

      // StringRef getPassName() const override {
      //  return "American Fuzzy Lop Instrumentation";
      // }

  };

}


char AFLCoverage::ID = 0;

// BKDR Hash
u32 BKDRHash(std::string funhash )
{
    u32 seed = 31;
    u32 hash = 0;

    for(int i=0;i<funhash.size();i++){
       hash = hash * seed +(funhash[i]);
    }
    return (hash & 0x7FFFFFFF);
}

bool AFLCoverage::runOnModule(Module &M) {

  LLVMContext &C = M.getContext();

  IntegerType *Int8Ty  = IntegerType::getInt8Ty(C);
  IntegerType *Int32Ty = IntegerType::getInt32Ty(C);

  /* Show a banner */

  char be_quiet = 0;

  if (isatty(2) && !getenv("AFL_QUIET")) {

    SAYF(cCYA "afl-llvm-pass " cBRI VERSION cRST " by <lszekeres@google.com>\n");

  } else be_quiet = 1;

  /* Decide instrumentation ratio */

  char* inst_ratio_str = getenv("AFL_INST_RATIO");
  unsigned int inst_ratio = 100;

  if (inst_ratio_str) {

    if (sscanf(inst_ratio_str, "%u", &inst_ratio) != 1 || !inst_ratio ||
        inst_ratio > 100)
      FATAL("Bad value of AFL_INST_RATIO (must be between 1 and 100)");

  }

  /* Get globals for the SHM region and the previous location. Note that
     __afl_prev_loc is thread-local. */

  GlobalVariable *AFLMapPtr =
      new GlobalVariable(M, PointerType::get(Int8Ty, 0), false,
                         GlobalValue::ExternalLinkage, 0, "__afl_area_ptr");

  GlobalVariable *AFLFunHitPtr = 
      new GlobalVariable(M, PointerType::get(Int32Ty,0), false,
                        GlobalValue::ExternalLinkage, 0, "__afl_function_hit_ptr");

  GlobalVariable *AFLPrevLoc = new GlobalVariable(
      M, Int32Ty, false, GlobalValue::ExternalLinkage, 0, "__afl_prev_loc",
      0, GlobalVariable::GeneralDynamicTLSModel, 0, false);

  /* Instrument all the things! */

  int inst_blocks = 0;

  for (auto &F : M){
    u32 funnamehash = BKDRHash(F.getName());
    // int block=0;
    SmallPtrSet<Instruction *, 32> instru_points;
    for (auto &BB : F) {

      BasicBlock::iterator IP = BB.getFirstInsertionPt();
      IRBuilder<> IRB(&(*IP));
      instru_points.insert(&(*IP));  

    }
    int block = 0;
    for (auto I = instru_points.begin(); I!= instru_points.end();++I)
    {
        IRBuilder<> IRB(*I);
        if (AFL_R(100) >= inst_ratio) continue;

        /* Make up cur_loc */

        unsigned int cur_loc = AFL_R(MAP_SIZE);

        ConstantInt *CurLoc = ConstantInt::get(Int32Ty, cur_loc);

        /* Load prev_loc */

        LoadInst *PrevLoc = IRB.CreateLoad(AFLPrevLoc);
        PrevLoc->setMetadata(M.getMDKindID("nosanitize"), MDNode::get(C, None));
        Value *PrevLocCasted = IRB.CreateZExt(PrevLoc, IRB.getInt32Ty());

        /* Load SHM pointer */

        LoadInst *MapPtr = IRB.CreateLoad(AFLMapPtr);
        MapPtr->setMetadata(M.getMDKindID("nosanitize"), MDNode::get(C, None));
        Value *MapPtrIdx =
            IRB.CreateGEP(MapPtr, IRB.CreateXor(PrevLocCasted, CurLoc));

        /* Update bitmap */

        LoadInst *Counter = IRB.CreateLoad(MapPtrIdx);
        Counter->setMetadata(M.getMDKindID("nosanitize"), MDNode::get(C, None));
        Value *Incr = IRB.CreateAdd(Counter, ConstantInt::get(Int8Ty, 1));
        IRB.CreateStore(Incr, MapPtrIdx)
            ->setMetadata(M.getMDKindID("nosanitize"), MDNode::get(C, None));

        /* Set prev_loc to cur_loc >> 1 */

        StoreInst *Store =
            IRB.CreateStore(ConstantInt::get(Int32Ty, cur_loc >> 1), AFLPrevLoc);
        Store->setMetadata(M.getMDKindID("nosanitize"), MDNode::get(C, None));

        inst_blocks++;
        if(block==0){
            LoadInst *AFLFunHitPtrInst = IRB.CreateLoad(AFLFunHitPtr);
            AFLFunHitPtrInst->setMetadata(M.getMDKindID("nosanitize"), MDNode::get(C, None));
            Value *index = ConstantInt::get(Type::getInt32Ty(F.getContext()), 0); 
            Value *AFLFunHitIndex = IRB.CreateGEP(AFLFunHitPtrInst,index);
            Value *asize = ConstantInt::get(Type::getInt32Ty(F.getContext()), 65535); 

            LoadInst *FunCounter = IRB.CreateLoad(AFLFunHitIndex);
            FunCounter->setMetadata(M.getMDKindID("nosanitize"), MDNode::get(C, None));
            
        
            Value* cmp = IRB.CreateICmpSLT(FunCounter, asize);
            Instruction *ifthen=SplitBlockAndInsertIfThen(cmp, (*I), false); 

            IRBuilder<> IRB2(ifthen);

            Value *FunCounterAdd = IRB2.CreateAdd(FunCounter, ConstantInt::get(Int32Ty, 1));
            IRB2.CreateStore(FunCounterAdd,AFLFunHitIndex)->setMetadata(M.getMDKindID("nosanitize"), MDNode::get(C, None));

            Value *StoreLocation = IRB2.CreateGEP(AFLFunHitPtrInst,FunCounterAdd);
            Value *StoreValue = ConstantInt::get(Type::getInt32Ty(F.getContext()), funnamehash); 
            IRB2.CreateStore(StoreValue,StoreLocation)->setMetadata(M.getMDKindID("nosanitize"), MDNode::get(C, None));

        }

        block++;
    }
  }
  /* Say something nice. */

  if (!be_quiet) {

    if (!inst_blocks) WARNF("No instrumentation targets found.");
    else OKF("Instrumented %u locations (%s mode, ratio %u%%).",
             inst_blocks, getenv("AFL_HARDEN") ? "hardened" :
             ((getenv("AFL_USE_ASAN") || getenv("AFL_USE_MSAN")) ?
              "ASAN/MSAN" : "non-hardened"), inst_ratio);

  }

  return true;

}


static void registerAFLPass(const PassManagerBuilder &,
                            legacy::PassManagerBase &PM) {

  PM.add(new AFLCoverage());

}


static RegisterStandardPasses RegisterAFLPass(
    PassManagerBuilder::EP_OptimizerLast, registerAFLPass);

static RegisterStandardPasses RegisterAFLPass0(
    PassManagerBuilder::EP_EnabledOnOptLevel0, registerAFLPass);
