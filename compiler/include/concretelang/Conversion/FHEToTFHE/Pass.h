// Part of the Concrete Compiler Project, under the BSD3 License with Zama
// Exceptions. See
// https://github.com/zama-ai/concrete-compiler-internal/blob/main/LICENSE.txt
// for license information.

#ifndef CONCRETELANG_CONVERSION_FHETOTFHE_PASS_H_
#define CONCRETELANG_CONVERSION_FHETOTFHE_PASS_H_

#include "mlir/Pass/Pass.h"

namespace mlir {
namespace concretelang {

// ApplyLookupTableLowering indicates the strategy to lower an
// FHE.apply_loopup_table ops
enum ApplyLookupTableLowering {
  KeySwitchBoostrapLowering,
  WopPBSLowering,
};

/// Create a pass to convert `FHE` dialect to `TFHE` dialect.
std::unique_ptr<OperationPass<ModuleOp>>
createConvertFHEToTFHEPass(ApplyLookupTableLowering lower);
} // namespace concretelang
} // namespace mlir

#endif
