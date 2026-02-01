#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <string.h>

void convolutionCPU(unsigned int *input, unsigned int *output, float *kernel, int M, int N) {
    int offset = N / 2;
    for (int i = 0; i < M; i++) {
        for (int j = 0; j < M; j++) {
            float sum = 0.0f;
            for (int ki = 0; ki < N; ki++) {
                for (int kj = 0; kj < N; kj++) {
                    int ii = i + ki - offset;
                    int jj = j + kj - offset;
                    if (ii >= 0 && ii < M && jj >= 0 && jj < M) {
                        sum += input[ii * M + jj] * kernel[ki * N + kj];
                    }
                }
            }
            if (sum < 0.0f) sum = 0.0f;
            if (sum > 255.0f) sum = 255.0f;
            output[i * M + j] = (unsigned int)sum;
        }
    }
}

unsigned int* readMatrix(const char *filename, int *M) {
    FILE *fp = fopen(filename, "r");
    if (!fp) return NULL;
    int cols;
    if (fscanf(fp, "%d %d", M, &cols) != 2) {
        fclose(fp);
        return NULL;
    }
    unsigned int *data = (unsigned int *)malloc(*M * *M * sizeof(unsigned int));
    for (int i = 0; i < *M * *M; i++) {
        fscanf(fp, "%u", &data[i]);
    }
    fclose(fp);
    return data;
}

void saveMatrix(const char *filename, unsigned int *data, int M) {
    FILE *fp = fopen(filename, "w");
    if (!fp) return;
    fprintf(fp, "%d %d\n", M, M);
    for (int i = 0; i < M * M; i++) {
        fprintf(fp, "%u ", data[i]);
        if ((i + 1) % M == 0) fprintf(fp, "\n");
    }
    fclose(fp);
}

float* generateFilter(int N) {
    float *filter = (float *)malloc(N * N * sizeof(float));
    if (N == 3) {
        float laplacian[9] = {0, -1, 0, -1, 4, -1, 0, -1, 0};
        memcpy(filter, laplacian, 9 * sizeof(float));
    } else {
        float val = 1.0f / (N * N);
        for (int i = 0; i < N * N; i++) {
            filter[i] = val;
        }
    }
    return filter;
}

int main(int argc, char **argv) {
    const char *input_files[] = {"../data/output_matrices/test_1.txt", "../data/output_matrices/test_2.txt", "../data/output_matrices/test_3.txt"};
    int filter_sizes[] = {3, 5, 7};
    int num_images = 3;
    int num_filters = 3;

    for (int i = 0; i < num_images; i++) {
        int M;
        unsigned int *h_input = readMatrix(input_files[i], &M);

        unsigned int *h_output = (unsigned int *)malloc(M * M * sizeof(unsigned int));

        for (int j = 0; j < num_filters; j++) {
            int N = filter_sizes[j];
            float *h_filter = generateFilter(N);

            clock_t start = clock();
            
            convolutionCPU(h_input, h_output, h_filter, M, N);

            clock_t end = clock();
            double time_taken = ((double)(end - start)) / CLOCKS_PER_SEC;

            printf("Image: %s (MxM: %dx%d) | Filter: %dx%d | Time: %f s\n", 
                   input_files[i], M, M, N, N, time_taken);

            char out_filename[64];
            sprintf(out_filename, "result_%d_N%d.txt", M, N);
            saveMatrix(out_filename, h_output, M);

            free(h_filter);
        }

        free(h_input);
        free(h_output);
    }

    return 0;
}