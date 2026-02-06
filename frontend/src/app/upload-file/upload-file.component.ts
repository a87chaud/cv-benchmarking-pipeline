import { Component, inject, OnInit, signal, Signal } from '@angular/core';
import { RUN_INFERENCE_URL } from '../constants';
import {
  ButtonGroupComponent,
  ButtonGroupConfig,
} from '../components/button-group-component/button-group-component';
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
  CLASSIFICATION = 'classification',
}

@Component({
  standalone: true,
  selector: 'app-upload-file',
  imports: [CommonModule, FormsModule],
  templateUrl: './upload-file.html',
  styleUrl: './upload-file.css',
})
// Component to handle single file uploads
// Currently the only info we want is the file
// Once the app grows we will get extra context which will help in training
export class UploadFile {
  inferenceService: InferenceService = inject(InferenceService);
  private sanitizer: DomSanitizer = inject(DomSanitizer);
  inferenceResponse = signal<InferenceResponse | undefined>(undefined);
  selectedFile: File | null = null;
  selectedAnnotation: File | null = null;
  response = signal<InferenceResponse | undefined>(undefined);

  selectedUseCase: ModelUsecases = ModelUsecases.DETETECTION;
  selectedPriority: string = 'medium';
  targetHardware: string = 'RPI';
  MODEL_USE_CASES = [
    { text: 'Detection', value: 'Detection' },
    { text: 'Classification', value: 'Classification' },
  ];
  latencyFps: number = 30;
  accuracyMap: number = 0.8;

  handleUsecaseSelection(usecase: string): void {
    this.selectedUseCase = usecase as ModelUsecases;
  }

  onFileSelected(event: any) {
    this.selectedFile = event.target.files[0];
  }

  onAnnotationSelected(event: any) {
    this.selectedAnnotation = event.target.files[0];
  }
  safeVideoUrl(res: any) {
    console.log('res: ', res);
    return this.sanitizer.bypassSecurityTrustResourceUrl(res.annotated_img_url);
  }

  async onUpload() {
    if (!this.selectedFile) return;

    try {
      const baseUrl = 'http://127.0.0.1:5000/s3';
      const fileName = (this.selectedFile as File).name;
      const annnotationFileName = (this.selectedAnnotation as File).name;

      const allFileUploads = [
        this.inferenceService.uploadFileToS3(baseUrl, this.selectedFile as File, fileName),
        this.inferenceService.uploadFileToS3(
          baseUrl,
          this.selectedAnnotation as File,
          annnotationFileName,
        ),
      ];

      const res = await Promise.all(allFileUploads);
      res.forEach((r) => {
        r.subscribe((rSub) => console.log(rSub));
      });

      // Step 2: Run Inference/Benchmarking
      // Now we just send the S3 Key and the metadata
      const inferencePayload = {
        file_s3_key: fileName,
        annotation_s3_key: annnotationFileName,
        model_use_case: this.selectedUseCase,
        target_latency: this.latencyFps,
        target_accuracy: this.accuracyMap,
        target_hardware: this.targetHardware,
      };

      const benchmarkingUrl = `${baseUrl}/inference/benchmarking`;

      // this.inferenceService.runInference(benchmarkingUrl, inferencePayload).subscribe({
      //   next: (res) => {
      //     this.inferenceResponse.set(res);
      //   },
      //   error: (e) => console.error('Inference failed:', e),
      // });
    } catch (error) {
      console.error('S3 Upload failed:', error);
    }
  }
}
