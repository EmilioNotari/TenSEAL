include(FetchContent)

set(SEAL_BUILD_DEPS ON)
set(SEAL_USE_MSGSL ON)
set(SEAL_USE_INTEL_HEXL OFF)

#LO HE COMENTADO YO
# FetchContent_Declare(
#   com_microsoft_seal
#   GIT_REPOSITORY https://github.com/microsoft/SEAL
#   GIT_TAG        v4.1.1
# )

#ESTO LO HE AÑADIDO YO
FetchContent_Declare(
    com_microsoft_seal
    SOURCE_DIR /home/enotari/Escritorio/SEAL
)

FetchContent_MakeAvailable(com_microsoft_seal)

include_directories(${com_microsoft_seal_SOURCE_DIR}/native/src)
include_directories(${com_microsoft_seal_SOURCE_DIR}/thirdparty/msgsl-src/include/)
include_directories(${com_microsoft_seal_SOURCE_DIR}/thirdparty/hexl-src/hexl/include/)
include_directories(${com_microsoft_seal_BINARY_DIR}/native/src)

message("USANDO SEAL DE: ${com_microsoft_seal_SOURCE_DIR}") 
