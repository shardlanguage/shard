#pragma once

#include "lexer/include/token_type.h"
#include <stdbool.h>

bool is_token_assignment_operator(TokenType token);
bool is_token_comparison_operator(TokenType token);