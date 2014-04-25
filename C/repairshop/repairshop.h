#include <string.h>
#include <stdio.h>

#define NAME_OF_CLIENT 26
#define PROBLEM_DESCRIPTION 81
#define SOLUTION_DESCRIPTION 256

#define BUFFER 400

typedef struct {
	char nameOfClient[NAME_OF_CLIENT];
	char problemDescription[PROBLEM_DESCRIPTION];
	char solutionDescription[SOLUTION_DESCRIPTION];
	int timeSpent;
} Trepair;

void init(Trepair repairs[], int size) {
	int i;
	Trepair defaults = {"", "", "", 0};

	for (i=0; i < size; ++i) {
		repairs[i] = defaults;
	}
}

void saveToDisk(Trepair repairs[], int size) {
	int i;
	FILE *file;
	file = fopen("data.dat", "w");
	for(i=0; i < size; ++i) {
		if (strlen(repairs[i].nameOfClient)) {
			fprintf(file, "%s |%s |%s |%d\n", repairs[i].nameOfClient, repairs[i].problemDescription, 
			repairs[i].solutionDescription, repairs[i].timeSpent);
		}
	}
	fclose(file);
}

void readFromDisk(Trepair repairs[], int size) {
	int i;
	FILE *file;
	char buffer[BUFFER];
	char *token;

	init(repairs, size);

	file = fopen("data.dat", "r");

	i = 0;
	while (fgets(buffer, BUFFER, file) != NULL) {
		token = strtok(buffer, "|");
		strcpy(repairs[i].nameOfClient, token);
		token = strtok(NULL, "|");
		strcpy(repairs[i].problemDescription, token);
		token = strtok(NULL, "|");
		strcpy(repairs[i].solutionDescription, token);
		token = strtok(NULL, "|");
		repairs[i].timeSpent = atoi(token);
		++i;
	}

	fclose(file);
}

void addNewTask(Trepair repairs[], char name[], char problem[]) {
	int i = 0, length = 0;
	
	do {
		length = strlen(repairs[i++].nameOfClient);
	} while (length > 0);

	--i;

	strcpy(repairs[i].nameOfClient, name);
	strcpy(repairs[i].problemDescription, problem);
	repairs[i].timeSpent = 0;
}


void performSolution(Trepair repairs[], int index, char solution[], int time) {
	strcpy(repairs[index-1].solutionDescription, solution);
	repairs[index-1].timeSpent = time;
}

void browseRepairs(Trepair repairs[], int size) {
	int i;
	for (i=0; i < size; ++i) {
		if (strlen(repairs[i].nameOfClient)) {
			printf("%d.\tName of client: %s\n\n\tDescription of problem\n\t%s\n\n\tSolution\n\t%s\n\n\tTime spent: %d minutes\n\n", 
			    i+1, repairs[i].nameOfClient, repairs[i].problemDescription, repairs[i].solutionDescription, repairs[i].timeSpent);
		}
	}
}

void mostTimeConsumingRepairs(Trepair repairs[], int size) {
	int i;
	int valueAndIndex[3][2] = {0};
	for (i=0; i < size; ++i) {
		if (repairs[i].timeSpent >= valueAndIndex[0][0]) {
			valueAndIndex[2][0] = valueAndIndex[1][0];
			valueAndIndex[2][1] = valueAndIndex[1][1];
			valueAndIndex[1][0] = valueAndIndex[0][0];
			valueAndIndex[1][1] = valueAndIndex[0][1];
			valueAndIndex[0][0] = repairs[i].timeSpent;
			valueAndIndex[0][1] = i;
			continue;
		}

		if (repairs[i].timeSpent >= valueAndIndex[1][0]) {
			valueAndIndex[2][0] = valueAndIndex[1][0];
			valueAndIndex[2][1] = valueAndIndex[1][1];
			valueAndIndex[1][0] = repairs[i].timeSpent;
			valueAndIndex[1][1] = i;
			continue;
		}

		if (repairs[i].timeSpent >= valueAndIndex[2][0]) {
			valueAndIndex[2][0] = repairs[i].timeSpent;
			valueAndIndex[2][1] = i;
		}
	}

	for (i=0; i < 3; ++i) {
	printf("%d.\tName of client: %s\n\n\tDescription of problem\n\t%s\n\n\tSolution\n\t%s\n\n\tTime spent: %d minutes\n\n", 
			i+1, repairs[valueAndIndex[i][1]].nameOfClient, repairs[valueAndIndex[i][1]].problemDescription, 
			repairs[valueAndIndex[i][1]].solutionDescription, repairs[valueAndIndex[i][1]].timeSpent);
	}
}


void printAllRepairsCompletedFirst(Trepair repairs[], int size) {
	int i;
	for (i=0; i < size; ++i) {
		if (repairs[i].timeSpent > 0) {
			printf("\tName of client: %s\n\n\tDescription of problem\n\t%s\n\n\tSolution\n\t%s\n\n\tTime spent: %d minutes\n\n", 
					repairs[i].nameOfClient, repairs[i].problemDescription, repairs[i].solutionDescription, repairs[i].timeSpent);
		}
	}

	for (i=0; i < size; ++i) {
		if (repairs[i].timeSpent == 0) {
			if (strlen(repairs[i].nameOfClient)) {
				printf("\tName of client: %s\n\n\tDescription of problem\n\t%s\n\n\tSolution\n\t%s\n\n\tTime spent: %d minutes\n\n", 
					repairs[i].nameOfClient, repairs[i].problemDescription, repairs[i].solutionDescription, repairs[i].timeSpent);
			}
		}
	}
}

