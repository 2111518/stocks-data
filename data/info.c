#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

#define NL 170  // 最大字串長度
#define MAX_FIELDS 20  // 假設最多 20 個欄位

// 定義鏈結串列節點
struct fdata {
    char line[NL];
    struct fdata *next;
};

typedef struct fdata fda;

int main() {
    FILE *fp = NULL;
    char buff[NL];
    int num = 0;

    fda *head = NULL, *tail = NULL, *temp = NULL;

    // 開啟檔案 constituents.csv
    fp = fopen("constituents.csv", "r");
    if (fp == NULL) {
        printf("無法開啟 constituents.csv\n");
        return 1;
    }

    // 讀取檔案並建立鏈結串列
    while (fgets(buff, NL, fp) != NULL) {
        temp = (fda *)malloc(sizeof(fda)); // 動態分配記憶體
        if (temp == NULL) {
            printf("記憶體分配失敗\n");
            return 1;
        }

        strncpy(temp->line, buff, NL - 1);
        temp->line[NL - 1] = '\0'; // 確保字串結尾
        temp->next = NULL;

        if (head == NULL) {
            head = tail = temp; // 第一個節點
        } else {
            tail->next = temp; // 新節點加入尾端
            tail = temp;
        }

        num++;
    }
    fclose(fp);

    // 開啟輸出檔案 test.txt
    fp = fopen("info.txt", "w+");
    if (fp == NULL) {
        printf("無法開啟 info.txt\n");
        return 1;
    }

    // 找出每個欄位的最長字串
    int maxz[MAX_FIELDS] = {0};
    int maxn = 0;  // 紀錄最大有效字串長度
    int len = 0; // 暫時存放字串長度
    temp = head;
    while (temp != NULL) {
        len = strlen(temp->line);
        if (len > maxn) {
            maxn = len;
        }

        // 計算各欄位最大長度
        int count = 0, start = 0;
        int field_len = 0;
        bool quote=false;
        for (int i = 0; temp->line[i] != '\0'; i++) {
            if(temp->line[i]=='\"'){
                quote = !quote;
            }
            if ((temp->line[i] == ',' && !quote)|| temp->line[i + 1] == '\0') {
                field_len = (temp->line[i + 1] == '\0') ? (i - start + 1) : (i - start);
                if (field_len > maxz[count]) {
                    maxz[count] = field_len;
                }
                count++;
                start = i + 1;
            }
            if (count >= MAX_FIELDS) {
                break;
            }
        }
        temp = temp->next;
    }

    // 輸出最大欄位長度
    const char *field_names[MAX_FIELDS] = {
        "Symbol", "Security", "GICS Sector", "GICS Sub-Industry",
        "Headquarters Location", "Date added", "CIK", "Founded"
    };
    int field_count = 8; // 預設為 8 個欄位

    for (int i = 0; i < field_count; i++) {
        fprintf(fp, "%s: %d\n", field_names[i], maxz[i]);
    }

    fprintf(fp, "\n資料行數: %d\n", num);
    fprintf(fp, "最大有效字串長度: %d\n", maxn);
    fclose(fp);

    // 釋放記憶體
    while (head != NULL) {
        temp = head;
        head = head->next;
        free(temp);
    }

    return 0;
}

