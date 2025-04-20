#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <stdbool.h>

struct data {
    char symbol[8];
    char name[40];
    char gics[25];
};
typedef struct data dt;

// 排序：先依 GICS，再依 Symbol
int compare(const void *a, const void *b) {
    const dt *x = (const dt *)a;
    const dt *y = (const dt *)b;

    int gics_cmp = strcmp(x->gics, y->gics);
    if (gics_cmp != 0) {
        return gics_cmp;
    }
    return strcmp(x->symbol, y->symbol);
}

// 將字串轉為小寫
void to_lower_str(char *str) {
    for (int i = 0; str[i]; i++) {
        str[i] = tolower(str[i]);
    }
}

// 判斷 GICS 是否在清單中
int is_gics_in_list(const char *gics, char gics_list[][25], int gics_count) {
    char temp[25];
    strncpy(temp, gics, sizeof(temp));
    temp[sizeof(temp) - 1] = '\0';
    to_lower_str(temp);

    for (int i = 0; i < gics_count; i++) {
        if (strcmp(temp, gics_list[i]) == 0) {
            return 1;
        }
    }
    return 0;
}

int main() {
    dt sym[504];
    FILE *fp = fopen("out.txt", "r");
    if (fp == NULL) {
        perror("無法開啟 out.txt");
        return 1;
    }

    char line[200];
    int count = 0;
    while (fgets(line, sizeof(line), fp) != NULL && count < 504) {
        line[strcspn(line, "\n")] = '\0';

        char *token = strtok(line, "@");
        if (token == NULL) continue;
        strncpy(sym[count].symbol, token, sizeof(sym[count].symbol));
        sym[count].symbol[sizeof(sym[count].symbol) - 1] = '\0';

        token = strtok(NULL, "@");
        if (token != NULL) {
            strncpy(sym[count].name, token, sizeof(sym[count].name));
            sym[count].name[sizeof(sym[count].name) - 1] = '\0';
        } else {
            sym[count].name[0] = '\0';
        }

        token = strtok(NULL, "");
        if (token != NULL) {
            strncpy(sym[count].gics, token, sizeof(sym[count].gics));
            sym[count].gics[sizeof(sym[count].gics) - 1] = '\0';
        } else {
            sym[count].gics[0] = '\0';
        }

        count++;
    }
    fclose(fp);

    qsort(sym, count, sizeof(dt), compare);

    // 使用者輸入 GICS
    char input[100];
    char gics_list[50][25]; // 最多 50 個 GICS
    int gics_count = 0;

    printf("請一行一行輸入 GICS 類別（輸入 exit 結束）：\n");
    while (1) {
        printf("> ");
        if (fgets(input, sizeof(input), stdin) == NULL) break;

        input[strcspn(input, "\n")] = '\0';
        char temp[100];
        strncpy(temp, input, sizeof(temp));
        temp[sizeof(temp) - 1] = '\0';
        to_lower_str(temp);

        if (strcmp(temp, "exit") == 0) {
            break;
        }

        strncpy(gics_list[gics_count], temp, sizeof(gics_list[gics_count]));
        gics_list[gics_count][sizeof(gics_list[gics_count]) - 1] = '\0';
        gics_count++;
    }

    // 開啟輸出檔案
    FILE *out_fp = fopen("result.txt", "w+");
    if (out_fp == NULL) {
        perror("無法開啟 result.txt");
        return 1;
    }

    // 顯示並寫入符合條件的公司
    bool found = false;
    for (int i = 0; i < count; i++) {
        if (is_gics_in_list(sym[i].gics, gics_list, gics_count)) {
            //fprintf(out_fp, "%s %s %s\n", sym[i].symbol, sym[i].name, sym[i].gics);
            fprintf(out_fp, "%s %s\n", sym[i].symbol, sym[i].name);
            found=true;
        }
    }

    fclose(out_fp);

    if (!found) {
        printf("找不到符合條件的公司\n");
    } else {
        printf("已將結果寫入 result.txt\n");
    }

    return 0;
}

