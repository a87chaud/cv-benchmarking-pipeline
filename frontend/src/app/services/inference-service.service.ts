import { HttpClient } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';
import { InferenceResponse } from '../upload-file/upload-file.component';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class InferenceService {
  private http = inject(HttpClient);

  runInference(url: string, data: any) : Observable<InferenceResponse>{
    console.log('url: ', url)
    return this.http.post<InferenceResponse>(url, data);
  }
}
