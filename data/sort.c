#include <stdio.h>
#include <stdlib.h>
#include <string.h>

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

    FILE *out_fp = fopen("sort.txt", "w+");
    if (out_fp == NULL) {
        perror("無法開啟 sort.txt");
        return 1;
    }

    for (int i = 0; i < count; i++) {
        fprintf(out_fp, "%s %s %s\n", sym[i].symbol, sym[i].name, sym[i].gics);
    }
    fclose(out_fp);

    return 0;
}

