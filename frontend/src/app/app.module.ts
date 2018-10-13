import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { AppComponent } from './app.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';

import { MatFormFieldModule, MatInputModule, MatButtonModule } from '@angular/material';
import { HttpClientModule } from '@angular/common/http';
import { DashboardComponent } from './dashboard/dashboard.component';
import { NewMessageComponent } from './new-message/new-message.component';
import { SettingsPageComponent } from './settings-page/settings-page.component';
import { LandingComponent } from './landing/landing.component';
import {MatCardModule} from '@angular/material/card';
import {AppRoutes} from './app.routing';
import { LocationStrategy, HashLocationStrategy} from '@angular/common';
import {MatToolbarModule} from '@angular/material/toolbar';
import { ModalViewComponent } from './modal-view/modal-view.component';

import {MatDialogModule} from '@angular/material/dialog';




@NgModule({
  declarations: [
    AppComponent,
    DashboardComponent,
    NewMessageComponent,
    SettingsPageComponent,
    LandingComponent,
    ModalViewComponent
  ],
  imports: [
    MatDialogModule,
    MatToolbarModule,
    MatCardModule,
    AppRoutes,
    HttpClientModule,
    MatInputModule,
    MatButtonModule,
    MatFormFieldModule,
    BrowserModule,
    BrowserAnimationsModule
  ],
  providers: [{provide: LocationStrategy, useClass: HashLocationStrategy}],
  bootstrap: [AppComponent],
  entryComponents:[ModalViewComponent]
})
export class AppModule { }
