#include <stdio.h>
#include <stdlib.h>
#include "shell_array.h"
#include "sequence.h"

long *Array_Load_From_File(char *filename, int *size)
{
  FILE *fp = fopen(filename,"rb");
  if(fp==NULL){*size=0; return NULL;}

  // figure out how many longs are in the file
  fseek(fp,0,SEEK_END);
  long fsz = ftell(fp);
  fseek(fp,0,SEEK_SET);
  int cnt = fsz / sizeof(long);

  long *arr = malloc(cnt * sizeof(long));
  if(arr==NULL){*size=0; fclose(fp); return NULL;}

  fread(arr, sizeof(long), cnt, fp);
  fclose(fp);
  *size = cnt;
  return arr;
}

int Array_Save_To_File(char *filename, long *array, int size)
{
  if(array==NULL) return -1;
  FILE *fp = fopen(filename,"wb");
  if(fp==NULL) return -1;
  int w = fwrite(array, sizeof(long), size, fp);
  fclose(fp);
  return w;
}

void Array_Shellsort(long *array, int size, long *n_comp)
{
  *n_comp = 0;
  int seqsz;
  long *seq = Generate_2p3q_Seq(size, &seqsz);

  if(seq==NULL){
    // couldnt get memory so just do normal bubble sort
    seqsz = 1;
    seq = malloc(sizeof(long));
    seq[0] = 1;
  }

  // go through each gap biggest to smallest
  for(int g = seqsz-1; g >= 0; g--){
    long gap = seq[g];
    int sorted = 0;
    long lastex = size;

    while(!sorted){
      sorted = 1;
      long lastel = lastex - 1;
      for(long i = gap; i <= lastel; i++){
          (*n_comp)++;
          if(array[i-gap] > array[i]){
            // swap em
            long tmp = array[i];
            array[i] = array[i-gap];
            array[i-gap] = tmp;
            lastex = i;
            sorted = 0;
          }
      }
    }
  }
  free(seq);
}
