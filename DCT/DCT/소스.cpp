#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

#define N				16
#define M_PIl			3.141592653589793238462643383279502884L /* pi */
#define PARAMETER		16

double getCval(int x, int y) {
	if (x == 0 && y == 0)
		return double(1) / double(N);
	else if (x != 0 && y != 0)
		return double(2) / double(N);
	else
		return sqrt(double(2)) / double(N);
}

int main()
{
	double dTestArray[N][N] = { 0, };
	double dDctArray[N][N] = { 0, };
	double dRdctArray[N][N] = { 0, };

	FILE* pOriginalFile = NULL;

	// ���� �� ������ binary ���� ����.
	fopen_s(&pOriginalFile, "./sample.jpg", "rb");

	if (pOriginalFile == NULL)
	{
		fputs("File error", stderr);
		exit(1);
	}

	// �� ���Ͽ� ���� ���� resolution ũ�⸸ŭ �Ҵ� �޴´�.
	int resoulution_size = 1280 * 720;
	int nFrameSize = resoulution_size + resoulution_size / 2;
	unsigned char* read_data_origin = new unsigned char[nFrameSize];
	int* transformed_data = new int[nFrameSize];
	unsigned char* restored_data = new unsigned char[nFrameSize];
	memset(read_data_origin, 0, nFrameSize);
	memset(transformed_data, 0, nFrameSize * sizeof(int));
	memset(restored_data, 0, nFrameSize);
	size_t n_size = 0;

	// �� �����Ӹ� ����
	n_size = fread(read_data_origin, sizeof(unsigned char), nFrameSize, pOriginalFile);
	fclose(pOriginalFile);

	// ������ �ȼ��� 16x16 �� ����, dct ��ȯ�Ͽ� ����
	int nIndex = 0;
	while (nIndex < nFrameSize) {
		int nX = (nIndex / N) % N;
		int nY = nIndex % N;
		dTestArray[nX][nY] = double(read_data_origin[nIndex]);
		nIndex++;

		if (nIndex % (N * N) != 0)
			continue;

		for (int x = 0; x < N; x++) {
			for (int y = 0; y < N; y++) {
				double dInputSum = 0;
				for (int i = 0; i < N; i++) {
					for (int j = 0; j < N; j++) {
						dInputSum += dTestArray[i][j] *
							cos(((2 * double(j) + 1) * double(y) * M_PIl) / (double(2) * double(N))) *
							cos(((2 * double(i) + 1) * double(x) * M_PIl) / (double(2) * double(N)));
					}
				}
				dDctArray[x][y] = (getCval(x, y) * dInputSum);
			}
		}

		for (int i = nIndex - (N * N); i < nIndex; i++) {
			nX = (i / N) % N;
			nY = i % N;
			transformed_data[i] = (int)((dDctArray[nX][nY]) / double(PARAMETER)); // ����ȭ
		}
	}

	// �� dct
	nIndex = 0;
	while (nIndex < nFrameSize) {
		int nX = (nIndex / N) % N;
		int nY = nIndex % N;
		dDctArray[nX][nY] = double(transformed_data[nIndex]) * double(PARAMETER); // ����ȭ�� ��ŭ �ٽ� ����
		nIndex++;

		if (nIndex % (N * N) != 0)
			continue;

		for (int i = 0; i < N; i++) {
			for (int j = 0; j < N; j++) {
				double dInputSum = 0;
				for (int x = 0; x < N; x++) {
					for (int y = 0; y < N; y++) {
						dInputSum += getCval(x, y) * dDctArray[x][y] *
							cos(((2 * double(j) + 1) * double(y) * M_PIl) / (double(2) * double(N))) *
							cos(((2 * double(i) + 1) * double(x) * M_PIl) / (double(2) * double(N)));
					}
				}
				dRdctArray[i][j] = dInputSum;
			}
		}

		for (int i = nIndex - (N * N); i < nIndex; i++) {
			nX = (i / N) % N;
			nY = i % N;
			restored_data[i] = (unsigned char)(dRdctArray[nX][nY]);
		}
	}

	// ������ ����
	FILE* pWriteFile = NULL;
	fopen_s(&pWriteFile, "./unexpected.jpg", "w");
	n_size = fwrite(restored_data, sizeof(unsigned char), nFrameSize, pOriginalFile);

	if (pWriteFile != NULL)
		fclose(pWriteFile);

	// RMSE���� ���Ѵ�.
	long long nTmp = 0;
	double dmse = 0;
	for (int i = 0; i < nFrameSize; i++)
		nTmp += (read_data_origin[i] - restored_data[i]) * (read_data_origin[i] - restored_data[i]);

	dmse = (double)nTmp / nFrameSize;
	printf("MSE �� : %f\n", dmse);

	delete[] read_data_origin;
	delete[] transformed_data;
	delete[] restored_data;

	getchar();

	return 0;
}