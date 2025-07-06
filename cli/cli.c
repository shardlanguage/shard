#include "cli/include/cli.h"
#include <utils/info.h>
#include "include/repl.h"
#include <stdio.h>
#include <string.h>
#include "eval/include/env.h"
#include <stdlib.h>
#include "parser/include/ast.h"
#include "parser/include/parser.h"
#include <lexer/include/lexer.h>

#include <stdlib.h>
#include <string.h>

char *strndup(const char *s, size_t n) {
    size_t len = strnlen(s, n);
    char *new_str = malloc(len + 1);
    if (!new_str) return NULL;
    memcpy(new_str, s, len);
    new_str[len] = '\0';
    return new_str;
}
int main(int argc, char *argv[])
{
    if (argc == 1)
    {
        char line[MAX_CHARS_PER_LINE];
        Env env = env_init();

        repl_welcome();

        while (1)
        {
            printf(">>> ");
            if (!fgets(line, MAX_CHARS_PER_LINE, stdin))
                break;

            if (line[0] == '\n')
                continue;

            line[strcspn(line, "\n")] = '\0';

            char *source = malloc(strlen(line) + 2);
            source[0] = ' ';
            strcpy(source + 1, line);
            lex(source);
            ASTNode *ast = parse(source);

            eval_and_print_statements(&env, ast);

            AST_free(ast);
            free(source);
        }
    }
    else if (argc > 1)
    {
        if (strcmp(argv[1], OPT_CODE) == 0)
        {
            if (argc < 3)
            {
                fprintf(stderr, "No code to execute.\n");
                exit(1);
            }

            Env env = env_init();

            char *raw = argv[2];
            char *source = malloc(strlen(raw) + 2);
            source[0] = ' ';
            strcpy(source + 1, raw);

            ASTNode *ast = parse(source);

            eval_and_print_statements(&env, ast);

            AST_free(ast);
            free(source);
        }
        else if (strcmp(argv[1], OPT_HELP) == 0)
        {
            printf("no argument:\t\tREPL\n"
                   OPT_HELP "\t\tDisplay this message\n"
                   OPT_VERSION "\t\tDisplay the version installed on your System\n"
                   OPT_LICENSE "\t\tDisplay the name of the license\n"
                   OPT_CREDITS "\t\tDisplay the credits (special thanks...)\n"
                   OPT_LINK "\t\tDisplay " LANG_NAME "-related links\n"
                   OPT_CODE" <code>\t\tRun code from the CLI\n"
                   OPT_FILE_SHORT " / " OPT_FILE_LONG "\t\tExecute source code from a file\n");
        }
        else if (strcmp(argv[1], OPT_FILE_SHORT) == 0 || strcmp(argv[1], OPT_FILE_LONG) == 0)
        {
            FILE *file = fopen(argv[2], "r");
            if (!file)
            {
                fprintf(stderr, "Unable to open file.\n");
                exit(1);
            }

            fseek(file, 0, SEEK_END);
            long flength = ftell(file);
            rewind(file);

            char *source = malloc(flength + 2);
            source[0] = ' ';
            fread(source + 1, 1, flength, file);
            source[flength + 1] = '\0';

            fclose(file);

            Env env = env_init();
            ASTNode *ast = parse(source);

            eval_and_print_statements(&env, ast);

            AST_free(ast);
            free(source);
        }
        else if (strcmp(argv[1], OPT_VERSION) == 0)
            printf("Version %s\n", LANG_VERSION);
        else if (strcmp(argv[1], OPT_LICENSE) == 0)
            printf("Released under %s license\n", LANG_LICENSE);
        else if (strcmp(argv[1], OPT_CREDITS) == 0)
            printf("tayoky:\nC1: Ported Shard to the Stanix operating system\n\n"
                           "dogvloppeur:\nC1: Made build files for Windows\n\n");
        else if (strcmp(argv[1], OPT_LINK) == 0)
            printf(LANG_LINK_GH"\n");
        else
        {
            fprintf(stderr, "Invalid option. Use" OPT_HELP "for a list of available options.\n");
            exit(1);
        }
    }

    return 0;
}
