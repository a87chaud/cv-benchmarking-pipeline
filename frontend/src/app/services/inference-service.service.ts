import { HttpClient } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';
import { InferenceResponse } from '../upload-file/upload-file.component';
import { firstValueFrom, map, Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class InferenceService {
  private http = inject(HttpClient);
  private CHUNK_SIZE = 10 * 1024 * 1024; // 10MB

  runInference(url: string, data: any): Observable<InferenceResponse> {
    console.log('url: ', url);
    return this.http.post<InferenceResponse>(url, data);
  }

  async uploadFileToS3(baseUrl: string, file: File, fileName: string) {
    // get the upload id
    const getUploadIdUrl = baseUrl + '/get-multipart-uid';
    const getUploadIdBody = {
      s3UploadKey: fileName,
    };
    const { uploadId }: any = await firstValueFrom(this.http.post(getUploadIdUrl, getUploadIdBody));

    // Make parallel reqs using Promise.all
    const allPromises = [];
    let partNumber = 1;

    for (let startPointer = 0; startPointer < file.size; startPointer += this.CHUNK_SIZE) {
      const rawChunk = file.slice(startPointer, startPointer + this.CHUNK_SIZE);
      allPromises.push(this.singleChunkUpload(baseUrl, file.name, uploadId, rawChunk, partNumber));
    }

    const parts = await Promise.all(allPromises);
    const sortedParts = parts.sort((a, b) => a.PartNumber - b.PartNumber);
    const body = {
      s3UploadKey: fileName,
      uploadId: uploadId,
      parts: sortedParts,
    };
    return await this.http.post(`${baseUrl}/complete-upload`, body);
  }

  // yes im lazy i will make the interfaces later
  async singleChunkUpload(
    baseUrl: string,
    fileName: string,
    uploadId: string,
    chunk: Blob,
    partNumber: number,
  ): Promise<any> {
    const body = {
      s3UploadKey: fileName,
      uploadId: uploadId,
      partNumber: partNumber,
    };
    const res: any = await firstValueFrom(this.http.post(`${baseUrl}/generate-part-url`, body));
    if (!res) {
      console.log('Fuck');
      return;
    }
    const response = await firstValueFrom(
      this.http.put(res.url, chunk, {
        observe: 'response',
        responseType: 'text',
      }),
    );

    const etag = response.headers.get('ETag')?.replace(/"/g, '');
    return { PartNumber: partNumber, ETag: etag };
  }
}
