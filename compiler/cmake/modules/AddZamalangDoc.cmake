include(AddMLIR)

function(add_zamalang_doc doc_filename output_file output_directory command)
    set(SAVED_MLIR_BINARY_DIR ${MLIR_BINARY_DIR})
    set(MLIR_BINARY_DIR ${ZAMALANG_BINARY_DIR})
    add_mlir_doc(${doc_filename} ${output_file} ${output_directory} ${command})
    set(MLIR_BINARY_DIR ${SAVED_MLIR_BINARY_DIR})
    unset(SAVED_MLIR_BINARY_DIR)
endfunction()
