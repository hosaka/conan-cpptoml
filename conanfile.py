#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, CMake, tools
import os


class CppTOMLConan(ConanFile):
    name = "cpptoml"
    version = "0.1.1"
    url = "https://github.com/bincrafters/conan-cpptoml"
    description = "cpptoml is a header-only library for parsing TOML"
    topics = ("toml")
    license = "MIT"
    exports = ["LICENSE.md"]
    exports_sources = ["CMakeLists.txt"]
    generators = "cmake"

    # Options may need to change depending on the packaged library.
    settings = "os", "arch", "compiler", "build_type"
    options = {"build_examples": [True, False]}
    default_options = ("build_examples=False", )

    # Custom attributes for Bincrafters recipe conventions
    source_subfolder = "source_subfolder"
    build_subfolder = "build_subfolder"

    def source(self):
        source_url = "https://github.com/skystrife/cpptoml/archive/v{}.tar.gz".format(self.version)
        tools.get(source_url, sha256="23af72468cfd4040984d46a0dd2a609538579c78ddc429d6b8fd7a10a6e24403")
        os.rename("cpptoml-{!s}".format(self.version), self.source_subfolder)

        tools.replace_in_file("{0}/CMakeLists.txt".format(self.source_subfolder),
            "list(APPEND CMAKE_MODULE_PATH ${CMAKE_CURRENT_SOURCE_DIR}/deps/meta-cmake)",
            "")

    def build(self):
        cmake = CMake(self)
        cmake.definitions["CPPTOML_BUILD_EXAMPLES"] = self.options.build_examples
        cmake.configure(build_folder=self.build_subfolder)
        cmake.build()
        cmake.install()

    def package(self):
        self.copy(pattern="LICENSE", dst="license", src=self.source_subfolder)
    
    def package_id(self):
        self.info.header_only()

