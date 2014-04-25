#include <stdlib.h>
#include "linkedlist.h"

int createNode(Tlist* node, void* element) {
	node = (Tlist*)malloc(sizeof(Tlist));
	
	if (node == NULL) return 1; //MALLOC FAILED, ABORT
	else {
		node->element = element;
		node->next = NULL;
		node->previous = NULL;
	}
	
	return 0;
}

/*  This function is used for adding nodes to existing lists.
	One of the two arguments should be non-null. If the first
	argument is non-null, the second argument is not evaluated
	for purposes of linking the node to the list. */

int addNode(Tlist* node, Tlist *precedingNode, Tlist *followingNode) {

	if (precedingNode == NULL && followingNode == NULL) return 1;

	else {
		if (precedingNode != NULL) {
			node->previous = precedingNode;
			node->next = precedingNode->next;
			precedingNode->next = node;
			return 0;
		}
		
		else {
			node->previous = followingNode->previous;
			node->next = followingNode;
			followingNode->previous = node;
			return 0;
		}
	}
}

int removeNode(Tlist *node) {
	Tlist *previous = node->previous;
	Tlist *next = node->next;

	previous->next = next;
	next->previous = previous;

	free(node->element);
	free(node);
}