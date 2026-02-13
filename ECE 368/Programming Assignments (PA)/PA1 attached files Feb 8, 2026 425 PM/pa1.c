
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "shell_array.h"
#include "shell_list.h"

int main(int argc, char *argv[])
{
  if(argc != 4){
    return EXIT_FAILURE;
  }

  if(strcmp(argv[1], "-a") == 0){
    // array mode
    int sz;
    long *arr = Array_Load_From_File(argv[2], &sz);
    if(arr==NULL){
      return EXIT_FAILURE;
    }

    long ncomp;
    Array_Shellsort(arr, sz, &ncomp);
    printf("%ld\n", ncomp);

    int saved = Array_Save_To_File(argv[3], arr, sz);
    free(arr);
    if(saved == -1){
      return EXIT_FAILURE;
    }

  }else if(strcmp(argv[1], "-l") == 0){
    // linked list mode
    int stat;
    Node *list = List_Load_From_File(argv[2], &stat);
    if(stat == -1){
      return EXIT_FAILURE;
    }

    long ncomp;
    list = List_Shellsort(list, &ncomp);
    printf("%ld\n", ncomp);

    int saved = List_Save_To_File(argv[3], list);

    // free the whole list
    Node *cur = list;
    while(cur != NULL){
      Node *tmp = cur;
      cur = cur->next;
      free(tmp);
    }

    if(saved == -1){
      return EXIT_FAILURE;
    }

  }else{
    return EXIT_FAILURE;
  }

  return EXIT_SUCCESS;
}
