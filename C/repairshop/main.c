#include <stdlib.h>
#include "repairshop.h"

#define REPAIRS_ARRAY 10
#define READ 1
#define INIT 2
#define BROWSE 3
#define ADDNEW 4
#define SOLUTION 5
#define DISPLAYALL 6
#define DISPLAYTOP3 7
#define SAVE 8
#define EXIT 9
#define TEMP 300


void menu(Trepair repairs[]);

int main(void) {
	int i = 0;
	Trepair* repairs = (Trepair*)malloc(sizeof(Trepair) * REPAIRS_ARRAY);

	init(repairs, REPAIRS_ARRAY);

	menu(repairs);

	return 0;
}

void menu(Trepair repairs[]) {
	int choice = 0;
	char temp[TEMP];
	char temp2[TEMP];
	int tempint;
	int tempint2;
	
	while (choice != 9) {
		printf("\n\nComputer repair logger\n\n\n1.Read from disk\n2.Initialise all values\n3.Browse repairs\n4.Add new task\n5.Perform solution\n");
		printf("6.Display all repairs, completed first\n7.Display top 3 most time consuming repairs\n8.Save to disk\n9.Exit\n");

		scanf("%d", &choice);

		switch (choice) {
			case READ:
				readFromDisk(repairs, REPAIRS_ARRAY);
				break;
			case INIT:
				init(repairs, REPAIRS_ARRAY);
				break;
			case BROWSE:
				browseRepairs(repairs, REPAIRS_ARRAY);
				break;
			case ADDNEW:
				printf("\n\nPlease enter the name of the client.\n\n");
				getchar();
				fgets(temp, TEMP, stdin);
				printf("\n\nPlease enter a description of the problem.\n\n");
				fgets(temp2, TEMP, stdin);
				addNewTask(repairs, temp, temp2);
				break;
			case SOLUTION:
				printf("\n\nPlease enter the index number of the task you wish to add a solution to.\n\n");
				scanf("%d", &tempint);
				printf("\n\nPlease enter a description of the solution.\n\n");
				getchar();
				fgets(temp, TEMP, stdin);
				printf("\n\nPlease enter how many minutes it took to solve.\n\n");
				scanf("%d", &tempint2);
				performSolution(repairs, tempint, temp, tempint2);
				break;
			case DISPLAYALL:
				printAllRepairsCompletedFirst(repairs, REPAIRS_ARRAY);
				break;
			case DISPLAYTOP3:
				mostTimeConsumingRepairs(repairs, REPAIRS_ARRAY);
				break;
			case SAVE:
				saveToDisk(repairs, REPAIRS_ARRAY);
				break;
			case EXIT:
				break;
			default:
				printf("\n\nPlease enter a number 1-9.\n\n");

		}

	}
}