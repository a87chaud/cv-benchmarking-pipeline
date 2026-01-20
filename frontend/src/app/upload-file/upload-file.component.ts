import { Component, inject, OnInit, signal, Signal } from '@angular/core';
import { RUN_INFERENCE_URL } from '../constants';
import { ButtonGroupComponent, ButtonGroupConfig } from '../components/button-group-component/button-group-component';
import { InferenceService } from '../services/inference-service.service';
import { DomSanitizer } from '@angular/platform-browser';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';

export interface InferenceResponse {
  processing_time_ms: number;
  objects_detected: number;
  annotated_img_url: string;
  model_use_case: string;
  target_hardware: string;
}

const enum ModelUsecases {
  DETETECTION = 'detection',
  CLASSIFICATION = 'classification'
}

@Component({
  standalone: true,
  selector: 'app-upload-file',
  imports: [CommonModule, FormsModule],
  templateUrl: './upload-file.html',
  styleUrl: './upload-file.css'
})
// Component to handle single file uploads
// Currently the only info we want is the file
// Once the app grows we will get extra context which will help in training
export class UploadFile{
  inferenceService: InferenceService = inject(InferenceService)
  private sanitizer: DomSanitizer = inject(DomSanitizer)
  inferenceResponse = signal<InferenceResponse | undefined>(undefined);
  selectedFile: Blob | null = null;
  response = signal<InferenceResponse | undefined>(undefined);

  selectedUseCase: ModelUsecases = ModelUsecases.DETETECTION
  selectedPriority: string = 'medium';
  targetHardware: string = 'RPI';
  MODEL_USE_CASES =  [
    {text: 'Detection', value: 'Detection'},
    {text: 'Classification', value: 'Classification'}
  ]
  latencyFps: number = 30;
  accuracyMap: number = 0.80;

  handleUsecaseSelection(usecase: string): void { 
    this.selectedUseCase = usecase as ModelUsecases
  }

  onFileSelected(event: any) {
    this.selectedFile = event.target.files[0]
  }
  safeVideoUrl(res: any) {
    console.log('res: ', res)
  return this.sanitizer.bypassSecurityTrustResourceUrl(
    res.annotated_img_url
  );
}

  onUpload() {
    if (!this.selectedFile) return;
    const formData = new FormData()
    formData.append('file', this.selectedFile)
    formData.append('model_use_case', this.selectedUseCase as string)
    formData.append('target_latency', this.latencyFps.toString());
    formData.append('target_accuracy', this.accuracyMap.toString());
    formData.append('target_hardware', this.targetHardware as string)
    console.log('formData: ', formData)
    const testingUrl = 'http://127.0.0.1:5000/inference/benchmarking'
    this.inferenceService.runInference(testingUrl, formData).subscribe({
      next: (res) => {
        this.inferenceResponse.set(res)
      },
      error: (e) => console.log(e)
    })
  }

}
