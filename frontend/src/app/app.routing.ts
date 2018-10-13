import { RouterModule, Routes } from '@angular/router';
import {LandingComponent} from './landing/landing.component';
import {NewMessageComponent} from './new-message/new-message.component';
export const AppRoutes = RouterModule.forRoot([
  { path: '', component: LandingComponent },
  { path: 'newMessage', component: NewMessageComponent }
]);
