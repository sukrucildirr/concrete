// Part of the Concrete Compiler Project, under the BSD3 License with Zama
// Exceptions. See
// https://github.com/zama-ai/concrete-compiler-internal/blob/main/LICENSE.txt
// for license information.

#ifndef CONCRETELANG_DIALECT_BCONCRETE_TRANSFORMS_PASSES_H_
#define CONCRETELANG_DIALECT_BCONCRETE_TRANSFORMS_PASSES_H_

#include "mlir/Pass/Pass.h"

#define GEN_PASS_CLASSES
#include "concretelang/Dialect/BConcrete/Transforms/Passes.h.inc"

namespace mlir {
namespace concretelang {
std::unique_ptr<OperationPass<ModuleOp>> createAddRuntimeContext();
std::unique_ptr<OperationPass<func::FuncOp>> createEliminateCRTOps();
std::unique_ptr<OperationPass<ModuleOp>> createAsyncOffload();
} // namespace concretelang
} // namespace mlir

#endif // CONCRETELANG_DIALECT_BCONCRETE_TRANSFORMS_PASSES_H_
