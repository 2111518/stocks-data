#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

#define NL 175  // 每行最大字串長度
#define DELIM ','  // CSV 分隔符號

// 定義鏈結串列節點
struct fdata {
    char symbol[8];   // 存放 Symbol 欄位
    char security[40]; // 存放 Security 欄位
    char GICS_Sector[25];
    struct fdata *next;
};

typedef struct fdata fda;

// 解析一行 CSV，將前三個欄位存入欄位陣列中
void parse_csv_line(const char *line, char fields[3][80]) {
    int field_idx = 0;
    int char_idx = 0;
    bool in_quotes = false;

    for (int i = 0; line[i] != '\0' && field_idx < 3; i++) {
        char c = line[i];

        if (c == '\"') {
            in_quotes = !in_quotes;  // 開始或結束引號
        } else if (c == DELIM && !in_quotes) {
            fields[field_idx][char_idx] = '\0'; // 完成一欄
            field_idx++;
            char_idx = 0;
        } else {
            if (char_idx < 79) {  // 限制最大長度
                fields[field_idx][char_idx++] = c;
            }
        }
    }
    fields[field_idx][char_idx] = '\0'; // 最後一欄也要結束字串
}

int main() {
    FILE *fp = NULL;
    char buff[NL];
    int num = 0;

    fda *head = NULL, *tail = NULL, *temp = NULL;

    // 開啟檔案
    fp = fopen("constituents.csv", "r");
    if (fp == NULL) {
        printf("無法開啟檔案\n");
        return 1;
    }

    char fields[3][80];  // 暫存解析後的三個欄位

    // 讀取檔案並建立鏈結串列
    while (fgets(buff, NL, fp) != NULL) {
        if (num == 0) {
            num++;
            continue;  // 跳過標題列
        }

        parse_csv_line(buff, fields);  // 解析這一行

        temp = (fda *)malloc(sizeof(fda));
        if (temp == NULL) {
            printf("記憶體分配失敗\n");
            return 1;
        }

        // Symbol 欄位（轉換 '.' -> '-'）
        strncpy(temp->symbol, fields[0], sizeof(temp->symbol) - 1);
        for (int i = 0; temp->symbol[i] != '\0'; i++) {
            if (temp->symbol[i] == '.') {
                temp->symbol[i] = '-';
            }
        }
        temp->symbol[sizeof(temp->symbol) - 1] = '\0';

        // Security 欄位
        strncpy(temp->security, fields[1], sizeof(temp->security) - 1);
        temp->security[sizeof(temp->security) - 1] = '\0';

        // GICS Sector 欄位
        strncpy(temp->GICS_Sector, fields[2], sizeof(temp->GICS_Sector) - 1);
        temp->GICS_Sector[sizeof(temp->GICS_Sector) - 1] = '\0';

        temp->next = NULL;

        if (head == NULL) {
            head = temp;
            tail = head;
        } else {
            tail->next = temp;
            tail = temp;
        }

        num++;
    }
    fclose(fp);

    // 輸出資料
    fp = fopen("out.txt", "w+");
    temp = head;
    while (temp != NULL) {
        fprintf(fp, "%s@%s@%s\n", temp->symbol, temp->security, temp->GICS_Sector);
        temp = temp->next;
    }

    // 釋放記憶體
    while (head != NULL) {
        temp = head;
        head = head->next;
        free(temp);
    }
    tail = NULL;
    return 0;
}

