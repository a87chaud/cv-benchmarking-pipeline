import { Component, inject, signal, Signal } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { toSignal } from '@angular/core/rxjs-interop';
import { RUN_INFERENCE_URL } from '../constants';

export interface InferenceResponse {
  processing_time_ms: number;
  objects_detected: number;
  annotated_img_url: string;
}

@Component({
  selector: 'app-upload-file',
  imports: [],
  templateUrl: './upload-file.html',
  styleUrl: './upload-file.css'
})
// Component to handle single file uploads
// Currently the only info we want is the file
// Once the app grows we will get extra context which will help in training
export class UploadFile {
  selectedFile: Blob | null = null;
  response = signal<InferenceResponse | undefined>(undefined);
  private http = inject(HttpClient);

  onFileSelected(event: any) {
    this.selectedFile = event.target.files[0]
  }

  onUpload() {
    if (!this.selectedFile) return;

    const formData = new FormData()
    formData.append('file', this.selectedFile)
    this.http.post<InferenceResponse>(RUN_INFERENCE_URL, formData).subscribe({
      next: ((res) => {
        this.response.set(res)
        console.log('Response: ', this.response)
      }),
      error: (err) => console.log(err)
    })
  }

}