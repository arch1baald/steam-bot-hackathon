import { RouterModule, Routes } from '@angular/router';
import {LandingComponent} from './landing/landing.component';
import {NewMessageComponent} from './new-message/new-message.component';

import {DashboardComponent} from './dashboard/dashboard.component';
import {SettingsPageComponent} from './settings-page/settings-page.component';
export const AppRoutes = RouterModule.forRoot([
  { path: '', component: LandingComponent },
  { path: 'newMessage', component: NewMessageComponent},
  { path: 'dashboard', component: DashboardComponent},
  { path: 'settings', component: SettingsPageComponent}
]);
