import ast


def print_ast():

    # Source code to be parsed
    source_code = """
from watching import OldSweetheart


class AvocadoSmall(OldSweetheart):
    Name = "avocado small"
    Id_ = "e5d5f1da-5a3d-4581-bce9-97fc79291b49"
    AcceptablePrice = 690
 """

    # Parse the source code into an AST
    parsed_ast = ast.parse(source_code)

    # Output the AST
    print(ast.dump(parsed_ast, indent=4))


def gen_py_file():
    # Create an AST node for a function definition
    function_def = ast.FunctionDef(
        name='greet',
        args=ast.arguments(
            posonlyargs=[],  # No positional-only arguments
            args=[ast.arg(arg='name', annotation=None)],  # Regular arguments
            vararg=None,  # No *args
            kwonlyargs=[],  # No keyword-only arguments
            kw_defaults=[],  # No defaults for keyword-only arguments
            kwarg=None,  # No **kwargs
            defaults=[]  # No default values for arguments
        ),
        body=[ast.Expr(
            value=ast.Call(
                func=ast.Name(id='print', ctx=ast.Load()),  # The print function
                args=[ast.JoinedStr(
                    values=[
                        ast.Constant(value="Hello, "),  # Constant string
                        ast.FormattedValue(
                            value=ast.Name(id='name', ctx=ast.Load()),
                            # Formatted value
                            conversion=-1
                        ),
                        ast.Constant(value="!")  # Constant string
                    ]
                )],
                keywords=[]  # No keyword arguments
            ),
            lineno=3, col_offset=4  # Line and column offsets for the expression
        )],
        decorator_list=[],  # No decorators
        lineno=2, col_offset=0
        # Line and column offsets for the function definition
    )
    # Convert the AST to Python code
    generated_code = ast.unparse(function_def)
    print("Generated Python Code:\n", generated_code)

    # Write the generated code to a file
    with open('generated_code.py', 'w') as file:
        file.write(generated_code)


if __name__ == '__main__':
    print_ast()
