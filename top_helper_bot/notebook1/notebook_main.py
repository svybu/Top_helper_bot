from .functions_new import parser_string, wrong_command
from .decorator import input_error


@input_error
def main():
    while True:
        u_input = input('Enter command ')
        handler, *args = parser_string(u_input)
        if handler == wrong_command:
            print('Wrong command(')
        elif handler == exit:
            print("Good bye!")
            break
        else:
            result = handler(*args)
            print(result)

#

if __name__ == '__main__':
   main()
