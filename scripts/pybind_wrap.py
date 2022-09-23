#!/usr/bin/env python3
"""
Helper script to wrap C++ to Python with Pybind.
This script is installed via CMake to the user's binary directory
and invoked during the wrapping by CMake.
"""

# pylint: disable=import-error

import argparse

from gtwrap.pybind_wrapper import PybindWrapper


def main():
    """Main runner."""
    arg_parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    arg_parser.add_argument("--src",
                            type=str,
                            required=True,
                            help="Input interface .i/.h file(s)")
    arg_parser.add_argument(
        "--module_name",
        type=str,
        required=True,
        help="Name of the Python module to be generated and "
        "used in the Python `import` statement.",
    )
    arg_parser.add_argument(
        "--out_file",
        type=str,
        required=True,
        help="Output cc file.",
    )
    arg_parser.add_argument(
        "--use-boost",
        action="store_true",
        help="using boost's shared_ptr instead of std's",
    )
    arg_parser.add_argument(
        "--top_module_namespaces",
        type=str,
        default="",
        help="C++ namespace for the top module, e.g. `ns1::ns2::ns3`. "
        "Only the content within this namespace and its sub-namespaces "
        "will be wrapped. The content of this namespace will be available at "
        "the top module level, and its sub-namespaces' in the submodules.\n"
        "For example, `import <module_name>` gives you access to a Python "
        "`<module_name>.Class` of the corresponding C++ `ns1::ns2::ns3::Class`"
        "and `from <module_name> import ns4` gives you access to a Python "
        "`ns4.Class` of the C++ `ns1::ns2::ns3::ns4::Class`. ",
    )
    arg_parser.add_argument(
        "--ignore",
        nargs='*',
        type=str,
        help="A space-separated list of classes to ignore. "
        "Class names must include their full namespaces.",
    )
    group = arg_parser.add_mutually_exclusive_group(required=False)
    group.add_argument("--is_submodule",
                            default=False,
                            action="store_true")
    group.add_argument(
        "--submodules",
        nargs="+",
        default = [],
        help="List of submodules",
    )

    arg_parser.add_argument(
        "--additional_headers",
        nargs="+",
        default=[],
    )
    arg_parser.add_argument(
        "--preamble_header",
        type=str,
        default="Preamble header to include for STL classes",
    )
    arg_parser.add_argument(
        "--specialization_header",
        type=str,
        default="Specialization header to include for STL classes",
    )
    arg_parser.add_argument(
        "--dependencies",
        nargs="+",
        default=[],
        help="Dependent libs to import",
    )
    args = arg_parser.parse_args()

    top_module_namespaces = args.top_module_namespaces.split("::")
    if top_module_namespaces[0]:
        top_module_namespaces = [''] + top_module_namespaces

    wrapper = PybindWrapper(
        module_name=args.module_name,
        use_boost=args.use_boost,
        top_module_namespaces=top_module_namespaces,
        ignore_classes=args.ignore,
        additional_headers=args.additional_headers,
        preample_header=args.preamble_header,
        specialization_header=args.specialization_header,
        dependencies=args.dependencies,
    )

    # Wrap the code and get back the cpp/cc code.
    wrapper.wrap(args.src, args.out_file, args.submodules, args.is_submodule)


if __name__ == "__main__":
    main()
