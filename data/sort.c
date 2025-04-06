#include <stdio.h>
#include <stdlib.h>
#include <string.h>

struct data {
    char symbol[8];
    char name[40];
};
typedef struct data dt;

// 比較函式供 qsort 使用（依照 symbol 排序）
int compare(const void *a, const void *b) {
    return strcmp(((dt *)a)->symbol, ((dt *)b)->symbol);
}

int main() {
    dt sym[504];
    FILE *fp = fopen("out.txt", "r");
    if (fp == NULL) {
        perror("無法開啟 out.txt");
        return 1;
    }

    char line[128];
    int count = 0;
    while (fgets(line, sizeof(line), fp) != NULL && count < 504) {
        // 去除換行符號
        line[strcspn(line, "\n")] = '\0';

        // 使用 strtok 拆字串
        char *token = strtok(line, " ");  // 第一個是 symbol
        if (token == NULL) continue;
        strncpy(sym[count].symbol, token, sizeof(sym[count].symbol));
        sym[count].symbol[sizeof(sym[count].symbol) - 1] = '\0';

        // 剩下的是 name，用 strtok(NULL, "") 抓剩下全部
        token = strtok(NULL, "");
        if (token != NULL) {
            strncpy(sym[count].name, token, sizeof(sym[count].name));
            sym[count].name[sizeof(sym[count].name) - 1] = '\0';
        } else {
            sym[count].name[0] = '\0'; // 沒有名稱也避免殘留亂碼
        }

        count++;
    }
    fclose(fp);

    // 排序
    qsort(sym, count, sizeof(dt), compare);

    // 輸出排序後的結果
    FILE *out_fp = fopen("out-sort.txt", "w");
    if (out_fp == NULL) {
        perror("無法開啟 out-sort.txt");
        return 1;
    }

    for (int i = 0; i < count; i++) {
        fprintf(out_fp, "%s %s\n", sym[i].symbol, sym[i].name);
    }
    fclose(out_fp);

    //printf("排序結果已寫入 out-sort.txt\n");

    return 0;
}

