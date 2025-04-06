#include <stdio.h>
#include <stdlib.h>
#include <string.h>

struct data {
    char st[7];
};
typedef struct data dt;

// 比較函式供 qsort 使用
int compare(const void *a, const void *b) {
    return strcmp(((dt *)a)->st, ((dt *)b)->st);
}

int main() {
    dt sym[504];
    FILE *fp = fopen("out.txt", "r");
    if (fp == NULL) {
        perror("無法開啟 out.txt");
        return 1;
    }

    int count = 0;
    while (fgets(sym[count].st, sizeof(sym[count].st), fp) != NULL && count < 504) {
        // 去除換行符號
        sym[count].st[strcspn(sym[count].st, "\n")] = '\0';
        count++;
    }
    fclose(fp);

    // 排序
    qsort(sym, count, sizeof(dt), compare);

    // 將排序後的結果寫入新檔案
    FILE *out_fp = fopen("out-sort.txt", "w");
    if (out_fp == NULL) {
        perror("無法開啟 out-sort.txt");
        return 1;
    }

    for (int i = 0; i < count; i++) {
        fprintf(out_fp, "%s\n", sym[i].st);
    }
    fclose(out_fp);

    //printf("排序結果已寫入 out-sort.txt\n");

    return 0;
}

