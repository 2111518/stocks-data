#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define NL 170  // 最大字串長度

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

    // 開啟檔案
    fp = fopen("constituents.csv", "r");
    if (fp == NULL) {
        printf("無法開啟檔案\n");
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
	
	//找出每一個部分最長的字串
    int maxz[8], count, bef;
	for(int i=0;i<8;i++){
		maxz[i]=0;
	}
	
    // 找出最大有效字串長度
    int maxn = 0;
    temp = head;
    while (temp != NULL) {
		count=0;
		bef=0;
        int len = strlen(temp->line);
        if (len > maxn) {
            maxn = len;
        }
		for(int i=0;i<170;i++){
			if((temp->line[i] == ',' || temp->line[i] == '\0')&& (i-bef)>maxz[count]){
				maxz[count]=i-bef;
				count++;
				bef=i;
			}else if(temp->line[i] == ',' || temp->line[i] == '\0'){
				count++;
				bef=i;
			}
			if(temp->line[i] == '\0'){
				break;
			}
		}
        temp = temp->next;
    }
	for(int i=0;i<8;i++){
		printf("%d ",maxz[i]);
	}
	printf("\n");
    printf("資料行數: %d\n", num);
    printf("最大有效字串長度: %d\n", maxn);

    // 釋放記憶體
    while (head != NULL) {
        temp = head;
        head = head->next;
        free(temp);
    }

    return 0;
}

