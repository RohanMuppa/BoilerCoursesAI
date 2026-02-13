#include <stdio.h>
#include <stdlib.h>
#include "shell_list.h"
#include "sequence.h"


Node *List_Load_From_File(char *filename, int *status)
{
  FILE *fp = fopen(filename, "rb");
  if(fp==NULL){*status = -1; return NULL;}

  // see how big the file is
  fseek(fp, 0, SEEK_END);
  long fsz = ftell(fp);
  fseek(fp, 0, SEEK_SET);
  int cnt = fsz / sizeof(long);

  if(cnt==0){
    fclose(fp);
    *status = 0;
    return NULL;
  }

  Node *head = NULL;
  Node *tail = NULL;

  for(int i = 0; i < cnt; i++){
    Node *nd = malloc(sizeof(Node));
    if(nd==NULL){
      // couldnt get memory, clean up everything
      while(head!=NULL){
        Node *tmp = head;
        head = head->next;
        free(tmp);
      }
      fclose(fp);
      *status = -1;
      return NULL;
    }
    fread(&(nd->value), sizeof(long), 1, fp);
    nd->next = NULL;

    if(head==NULL){
      head = nd;
      tail = nd;
    }else{
      tail->next = nd;
      tail = nd;
    }
  }

  fclose(fp);
  *status = 0;
  return head;
}


int List_Save_To_File(char *filename, Node *list)
{
  FILE *fp = fopen(filename, "wb");
  if(fp==NULL) return -1;

  int cnt = 0;
  Node *cur = list;
  while(cur!=NULL){
    fwrite(&(cur->value), sizeof(long), 1, fp);
    cnt++;
    cur = cur->next;
  }
  fclose(fp);
  return cnt;
}


// helper to swap two nodes in the list
// pl is the node before left, pr is the node before right
// gap tells us if theyre next to each other or not
static void swap_nodes(Node *pl, Node *left, Node *pr, Node *right, int adjacent)
{
  Node *rn = right->next;

  if(adjacent){
    // left and right are right next to each other
    pl->next = right;
    left->next = rn;
    right->next = left;
  }else{
    // theres stuff between them
    Node *ln = left->next;
    pl->next = right;
    right->next = ln;
    pr->next = left;
    left->next = rn;
  }
}


Node *List_Shellsort(Node *list, long *n_comp)
{
  *n_comp = 0;

  // count how many nodes there are
  int n = 0;
  Node *c = list;
  while(c!=NULL){ n++; c = c->next; }

  if(n <= 1) return list;

  int seqsz;
  long *seq = Generate_2p3q_Seq(n, &seqsz);
  if(seq==NULL){
    seqsz = 1;
    seq = malloc(sizeof(long));
    if(seq==NULL) return list;
    seq[0] = 1;
  }

  // dummy node so we dont have to worry about the head changing
  Node dum;
  dum.value = 0;
  dum.next = list;

  // go through gaps biggest to smallest
  for(int g = seqsz - 1; g >= 0; g--){
    long gap = seq[g];
    int done = 0;
    int lim = n;

    while(!done){
      done = 1;
      int lastsw = 0;

      // set up left pointer at position 0
      Node *pl = &dum;
      Node *left = dum.next;

      // walk right pointer to position gap
      Node *pr = NULL;
      Node *right = left;
      long p;
      for(p = 0; p < gap; p++){
        if(right==NULL) break;
        pr = right;
        right = right->next;
      }
      if(right==NULL) break;

      int pos = (int)gap;

      // walk through the list comparing things gap apart
      while(right!=NULL && pos < lim){
        (*n_comp)++;

        if(left->value > right->value){
          done = 0;
          lastsw = pos;

          int adj = (pr == left);
          swap_nodes(pl, left, pr, right, adj);

          if(adj){
            // after swap right is before left now
            pl = right;
            pr = left;
            right = left->next;
          }else{
            // right jumped to where left was and vice versa
            pl = right;
            Node *nl = right->next;
            pr = left;
            right = left->next;
            left = nl;
          }
        }else{
          // theyre fine just move forward
          pl = left;
          left = left->next;
          pr = right;
          right = right->next;
        }
        pos++;
      }

      if(lastsw > 0) lim = lastsw;
    }
  }

  free(seq);
  return dum.next;
}
