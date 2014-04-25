
typedef struct {
	void *element;
	Tlist *next;
	Tlist *previous;
} Tlist;

int createNode(Tlist* node, void* element);

int addNode(Tlist* node, Tlist *precedingNode, Tlist *followingNode);

int removeNode(Tlist *node);