#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define NL 170  // 每行最大字串長度
#define DELIM ","  // CSV 分隔符號

// 定義鏈結串列節點
struct fdata {
    char symbol[8];   // 存放 Symbol 欄位
    char security[40]; // 存放 Security 欄位
    struct fdata *next;
};

typedef struct fdata fda;

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
	char *token = NULL;
    // 讀取檔案並建立鏈結串列
	while (fgets(buff, NL, fp) != NULL) {
		if(num==0){
			num++;
			continue;
		}
        
		temp = (fda *)malloc(sizeof(fda)); // 動態分配記憶體
		if (temp == NULL) {
			printf("記憶體分配失敗\n");
			return 1;
		}
		
		// 使用 strtok() 解析 CSV
		token = strtok(buff, DELIM);
			if (token != NULL) {
			strncpy(temp->symbol, token, sizeof(temp->symbol) - 1);
			for(int i=0;temp->symbol[i] != '\0';i++){
				if(temp->symbol[i] == '.'){
					temp->symbol[i] = '-';
				}
			}
            temp->symbol[sizeof(temp->symbol) - 1] = '\0'; // 確保字串結尾
		} else {
			strcpy(temp->symbol, "N/A"); // 若找不到則填入 "N/A"
		}

        token = strtok(NULL, DELIM);
        if (token != NULL) {
            strncpy(temp->security, token, sizeof(temp->security) - 1);
            temp->security[sizeof(temp->security) - 1] = '\0';
        } else {
            strcpy(temp->security, "N/A");
        }

		temp->next = NULL;

		if (head == NULL) {// 第一個節點
			head = temp;
			tail = head;
		} else {
			tail->next = temp; // 新節點加入尾端
			tail = temp;
		}

		num++;
	}
    fclose(fp);
    
    fp = NULL;
    fp = fopen("out.txt", "w+");
    // 輸出解析後的 Symbol 和 Security
    //printf("解析後的 Symbol 和 Security:\n");
    temp = head;
    while (temp != NULL) {
        fprintf(fp, "%s %s\n", temp->symbol, temp->security);
        //fprintf(fp, "%s\n", temp->symbol);
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
