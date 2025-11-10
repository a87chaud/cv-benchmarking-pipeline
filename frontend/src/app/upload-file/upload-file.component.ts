import { Component, inject, OnInit, signal, Signal } from '@angular/core';
import { RUN_INFERENCE_URL } from '../constants';
import { ButtonGroupComponent, ButtonGroupConfig } from '../components/button-group-component/button-group-component';
import { InferenceService } from '../services/inference-service.service';

export interface InferenceResponse {
  processing_time_ms: number;
  objects_detected: number;
  annotated_img_url: string;
  model_use_case: string;
}

const enum ModelUsecases {
  DETETECTION = 'detection',
  CLASSIFICATION = 'classification'
}

@Component({
  selector: 'app-upload-file',
  imports: [ButtonGroupComponent],
  templateUrl: './upload-file.html',
  styleUrl: './upload-file.css'
})
// Component to handle single file uploads
// Currently the only info we want is the file
// Once the app grows we will get extra context which will help in training
export class UploadFile{
  inferenceService: InferenceService = inject(InferenceService)
  inferenceResponse = signal<InferenceResponse | undefined>(undefined);
  selectedFile: Blob | null = null;
  response = signal<InferenceResponse | undefined>(undefined);
  modelUseCases: ButtonGroupConfig[] = [
    {text: 'Detection', value: 'detection'},
    {text: 'Classification', value: 'classification'}
  ]
  selectedUseCase: ModelUsecases = ModelUsecases.DETETECTION

  handleUsecaseSelection(usecase: string): void {
    this.selectedUseCase = usecase as ModelUsecases
  }

  onFileSelected(event: any) {
    this.selectedFile = event.target.files[0]
  }

  onUpload() {
    if (!this.selectedFile) return;
    const formData = new FormData()
    formData.append('file', this.selectedFile)
    formData.append('model_use_case', this.selectedUseCase as string)
    console.log('formData: ', formData)
    const testingUrl = 'http://127.0.0.1:5000/pre-process'
    this.inferenceService.runInference(testingUrl, formData).subscribe({
      next: (res) => {
        this.inferenceResponse.set(res)
      },
      error: (e) => console.log(e)
    })
  }

}
