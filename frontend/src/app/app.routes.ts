import { Routes } from '@angular/router';
import { UploadFile } from './upload-file/upload-file.component';
import { LoginComponent } from './components/login/login';
import { SignupComponent } from './components/signup/signup';
import { HomePage } from './home-page/home-page';
export const routes: Routes = [
    {path: 'upload', component: UploadFile},
    {path: "", component:HomePage},
    { path: 'login', component: LoginComponent },
    { path: 'signup', component: SignupComponent },
];
