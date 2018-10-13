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
import {AppRoutes} from './app.routing';
import { LocationStrategy, HashLocationStrategy} from '@angular/common';




@NgModule({
  declarations: [
    AppComponent,
    DashboardComponent,
    NewMessageComponent,
    SettingsPageComponent,
    LandingComponent
  ],
  imports: [
    AppRoutes,
    HttpClientModule,
    MatInputModule,
    MatButtonModule,
    MatFormFieldModule,
    BrowserModule,
    BrowserAnimationsModule
  ],
  providers: [{provide: LocationStrategy, useClass: HashLocationStrategy}],
  bootstrap: [AppComponent]
})
export class AppModule { }
