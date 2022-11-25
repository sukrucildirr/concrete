extern crate bindgen;

use std::env;
use std::error::Error;
use std::path::Path;
use std::process::exit;

const MLIR_STATIC_LIBS: [&str; 179] = [
    "MLIRMemRefDialect",
    "MLIRVectorToSPIRV",
    "MLIRControlFlowInterfaces",
    "MLIRLinalgToStandard",
    "MLIRAnalysis",
    "MLIRSPIRVDeserialization",
    "MLIRTransformDialect",
    "MLIRSparseTensorPipelines",
    "MLIRVectorToGPU",
    "MLIRTranslateLib",
    "MLIRPass",
    "MLIRComplexToLibm",
    "MLIRInferTypeOpInterface",
    "MLIRMemRefToSPIRV",
    "MLIRAMDGPUToROCDL",
    "MLIRBufferizationTransformOps",
    "MLIRExecutionEngineUtils",
    "MLIRNVVMDialect",
    "MLIRSCFUtils",
    "MLIRLinalgTransforms",
    "MLIRParser",
    "MLIRFuncTransforms",
    "MLIRTosaTestPasses",
    "MLIRTosaToArith",
    "MLIRTensorDialect",
    "MLIRGPUTransforms",
    "MLIRLowerableDialectsToLLVM",
    "MLIRBufferizationToMemRef",
    "MLIRPresburger",
    "MLIRFuncDialect",
    "MLIRPDLToPDLInterp",
    "MLIRArithmeticTransforms",
    "MLIRViewLikeInterface",
    "MLIRTargetCpp",
    "MLIROpenMPToLLVM",
    "MLIRSPIRVConversion",
    "MLIRNVGPUTransforms",
    "MLIRSparseTensorTransforms",
    "MLIRAffineAnalysis",
    "MLIRArmSVETransforms",
    "MLIRArmNeon2dToIntr",
    "MLIRDataLayoutInterfaces",
    "MLIRAffineTransforms",
    "MLIROpenACCToLLVMIRTranslation",
    "MLIRTensorUtils",
    "MLIRSPIRVSerialization",
    "MLIRShapeToStandard",
    "MLIRArithmeticToSPIRV",
    "MLIRArithmeticDialect",
    "MLIRFuncToSPIRV",
    "MLIRQuantUtils",
    "MLIRTensorTilingInterfaceImpl",
    "MLIRX86VectorToLLVMIRTranslation",
    "MLIRCopyOpInterface",
    "MLIRMathToLibm",
    "MLIRGPUToGPURuntimeTransforms",
    "MLIRLLVMDialect",
    "MLIRAffineDialect",
    "MLIRTransforms",
    "MLIRVectorTransforms",
    "MLIROpenMPDialect",
    "MLIRControlFlowDialect",
    "MLIRVectorUtils",
    "MLIRROCDLDialect",
    "MLIRPDLDialect",
    "MLIRAsyncDialect",
    "MLIRLinalgToLLVM",
    "MLIROpenACCDialect",
    "MLIRVectorDialect",
    "MLIROpenACCToSCF",
    "MLIRIR",
    "MLIRCAPIIR",
    "MLIRTargetLLVMIRImport",
    "MLIRTensorToLinalg",
    "MLIRCallInterfaces",
    "MLIRTensorInferTypeOpInterfaceImpl",
    "MLIRTransformDialectTransforms",
    "MLIRComplexDialect",
    "MLIRAffineUtils",
    "MLIRLoopLikeInterface",
    "MLIRDialect",
    "MLIRLinalgUtils",
    "MLIRSCFToSPIRV",
    "MLIRAffineToStandard",
    "MLIRX86VectorDialect",
    "MLIRGPUToVulkanTransforms",
    "MLIRRewrite",
    "MLIRAMXToLLVMIRTranslation",
    "MLIRInferIntRangeInterface",
    "MLIRCAPIRegistration",
    "MLIRNVVMToLLVMIRTranslation",
    "MLIRAsyncTransforms",
    "MLIRPDLInterpDialect",
    "MLIRTransformUtils",
    "MLIRLinalgDialect",
    "MLIRMathDialect",
    "MLIRMemRefTransforms",
    "MLIRSPIRVModuleCombiner",
    "MLIRMathToLLVM",
    "MLIRControlFlowToLLVM",
    "MLIRArmSVEDialect",
    "MLIRSPIRVTranslateRegistration",
    "MLIRToLLVMIRTranslationRegistration",
    "MLIRSCFDialect",
    "MLIRTilingInterface",
    "MLIREmitCDialect",
    "MLIRTableGen",
    "MLIRTosaToSCF",
    "MLIROpenMPToLLVMIRTranslation",
    "MLIRSupport",
    "MLIROpenACCToLLVM",
    "MLIRAMDGPUDialect",
    "MLIRTosaToLinalg",
    "MLIRSparseTensorUtils",
    "MLIRFuncToLLVM",
    "MLIRTargetLLVMIRExport",
    "MLIRControlFlowToSPIRV",
    "MLIRReconcileUnrealizedCasts",
    "MLIRComplexToStandard",
    "MLIRMathTransforms",
    "MLIRSPIRVUtils",
    "MLIRCastInterfaces",
    "MLIRTosaToTensor",
    "MLIRMemRefUtils",
    "MLIRGPUToSPIRV",
    "MLIRBufferizationDialect",
    "MLIRSCFToControlFlow",
    "MLIRArmSVEToLLVMIRTranslation",
    "MLIRExecutionEngine",
    "MLIRBufferizationTransforms",
    "MLIRSparseTensorDialect",
    "MLIRTensorToSPIRV",
    "MLIRVectorToSCF",
    "MLIRQuantTransforms",
    "MLIRLLVMToLLVMIRTranslation",
    "MLIRNVGPUDialect",
    "MLIRAsyncToLLVM",
    "MLIRAMXDialect",
    "MLIRLinalgTransformOps",
    "MLIRMathToSPIRV",
    "MLIRSCFToOpenMP",
    "MLIRShapeDialect",
    "MLIRGPUToROCDLTransforms",
    "MLIRGPUToNVVMTransforms",
    "MLIRTensorTransforms",
    "MLIRSCFToGPU",
    "MLIRDialectUtils",
    "MLIRNVGPUToNVVM",
    "MLIRTosaDialect",
    "MLIRVectorToLLVM",
    "MLIRSPIRVDialect",
    "MLIRSideEffectInterfaces",
    "MLIRVectorToROCDL",
    "MLIRQuantDialect",
    "MLIRSCFTransforms",
    "MLIRMLProgramDialect",
    "MLIRLinalgToSPIRV",
    "MLIRDLTIDialect",
    "MLIRLinalgFrontend",
    "MLIRROCDLToLLVMIRTranslation",
    "MLIRArmNeonDialect",
    "MLIRSPIRVToLLVM",
    "MLIRLLVMIRTransforms",
    "MLIRTosaTransforms",
    "MLIRLLVMCommonConversion",
    "MLIRSCFTransformOps",
    "MLIRArmNeonToLLVMIRTranslation",
    "MLIRAMXTransforms",
    "MLIRSPIRVTransforms",
    "MLIRMemRefToLLVM",
    "MLIRSPIRVBinaryUtils",
    "MLIRLinalgAnalysis",
    "MLIRArithmeticUtils",
    "MLIRVectorInterfaces",
    "MLIRGPUOps",
    "MLIRComplexToLLVM",
    "MLIRShapeOpsTransforms",
    "MLIRX86VectorTransforms",
    "MLIRArithmeticToLLVM",
];

const LLVM_STATIC_LIBS: [&str; 51] = [
    "LLVMAggressiveInstCombine",
    "LLVMAnalysis",
    "LLVMAsmParser",
    "LLVMAsmPrinter",
    "LLVMBinaryFormat",
    "LLVMBitReader",
    "LLVMBitstreamReader",
    "LLVMBitWriter",
    "LLVMCFGuard",
    "LLVMCodeGen",
    "LLVMCore",
    "LLVMCoroutines",
    "LLVMDebugInfoCodeView",
    "LLVMDebugInfoDWARF",
    "LLVMDebugInfoMSF",
    "LLVMDebugInfoPDB",
    "LLVMDemangle",
    "LLVMExecutionEngine",
    "LLVMFrontendOpenMP",
    "LLVMGlobalISel",
    "LLVMInstCombine",
    "LLVMInstrumentation",
    "LLVMipo",
    "LLVMIRReader",
    "LLVMJITLink",
    "LLVMLinker",
    "LLVMMC",
    "LLVMMCDisassembler",
    "LLVMMCParser",
    "LLVMObjCARCOpts",
    "LLVMObject",
    "LLVMOrcJIT",
    "LLVMOrcShared",
    "LLVMOrcTargetProcess",
    "LLVMPasses",
    "LLVMProfileData",
    "LLVMRemarks",
    "LLVMRuntimeDyld",
    "LLVMScalarOpts",
    "LLVMSelectionDAG",
    "LLVMSupport",
    "LLVMSymbolize",
    "LLVMTableGen",
    "LLVMTableGenGlobalISel",
    "LLVMTarget",
    "LLVMTextAPI",
    "LLVMTransformUtils",
    "LLVMVectorize",
    "LLVMX86CodeGen",
    "LLVMX86Desc",
    "LLVMX86Info",
];

const CONCRETE_COMPILER_LIBS: [&str; 31] = [
    "RTDialect",
    "RTDialectTransforms",
    "ConcretelangSupport",
    "BConcreteToCAPI",
    "ConcretelangConversion",
    "ConcretelangTransforms",
    "FHETensorOpsToLinalg",
    "ConcretelangServerLib",
    "ConcreteToBConcrete",
    "CONCRETELANGCAPIFHE",
    "TFHEGlobalParametrization",
    "ConcretelangClientLib",
    "ConcretelangBConcreteTransforms",
    "ConcretelangSDFGInterfaces",
    "CONCRETELANGCAPISupport",
    "FHELinalgDialect",
    "ConcretelangInterfaces",
    "TFHEDialect",
    "CONCRETELANGCAPIFHELINALG",
    "FHELinalgDialectTransforms",
    "FHEDialect",
    "TFHEToConcrete",
    "FHEToTFHE",
    "ConcreteDialectTransforms",
    "BConcreteDialect",
    "concrete_optimizer",
    "LinalgExtras",
    "FHEDialectAnalysis",
    "ConcreteDialect",
    "RTDialectAnalysis",
    "SDFGDialect"
];

fn main() {
    if let Err(error) = run() {
        eprintln!("{}", error);
        exit(1);
    }
}

fn run() -> Result<(), Box<dyn Error>> {
    let mut include_paths = Vec::new();
    // if set, use installation path of concrete compiler to lookup libraries and include files
    match env::var("CONCRETE_COMPILER_INSTALL_DIR") {
        Ok(install_dir) => {
            println!("cargo:rustc-link-search={}/lib/", install_dir);
            include_paths.push(Path::new(&format!("{}/include/", install_dir)).to_path_buf());
        }
        Err(_e) => println!(
            "cargo:warning=You are not setting CONCRETE_COMPILER_INSTALL_DIR, \
so your compiler/linker will have to lookup libs and include dirs on their own"
        ),
    }
    // linking
    // concrete-compiler libs
    for concrete_compiler_lib in CONCRETE_COMPILER_LIBS {
        println!("cargo:rustc-link-lib=static={}", concrete_compiler_lib);
    }
    // concrete compiler runtime
    println!("cargo:rustc-link-lib=ConcretelangRuntime");
    // concrete optimizer
    // `-bundle` serve to not have multiple definition issues
    println!("cargo:rustc-link-lib=static:-bundle=concrete_optimizer_cpp");
    // mlir libs
    for mlir_static_lib in MLIR_STATIC_LIBS {
        println!("cargo:rustc-link-lib=static={}", mlir_static_lib);
    }
    // llvm libs
    for llvm_static_lib in LLVM_STATIC_LIBS {
        println!("cargo:rustc-link-lib=static={}", llvm_static_lib);
    }
    // required by llvm
    println!("cargo:rustc-link-lib=tinfo");
    if let Some(name) = get_system_libcpp() {
        println!("cargo:rustc-link-lib={}", name);
    }
    // zlib
    println!("cargo:rustc-link-lib=z");

    println!("cargo:rerun-if-changed=api.h");
    bindgen::builder()
        .header("api.h")
        .clang_args(
            include_paths
                .into_iter()
                .map(|path| format!("-I{}", path.to_str().unwrap())),
        )
        .parse_callbacks(Box::new(bindgen::CargoCallbacks))
        .generate()
        .unwrap()
        .write_to_file(Path::new(&env::var("OUT_DIR")?).join("bindings.rs"))?;

    Ok(())
}

fn get_system_libcpp() -> Option<&'static str> {
    if cfg!(target_env = "msvc") {
        None
    } else if cfg!(target_os = "macos") {
        Some("c++")
    } else {
        Some("stdc++")
    }
}
