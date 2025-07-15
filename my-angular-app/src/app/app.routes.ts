import { Routes } from '@angular/router';
import { PropertyFormComponent } from './property-form/property-form.component';
import { MapsComponent } from './maps/maps.component';
import { ScrollingComponent } from './scrolling/scrolling.component';
import { LLMComponent } from './llm/llm.component';
import { PictureComponent } from './picture/picture.component';

export const routes: Routes = [
    { path: 'maps', component: MapsComponent },
    { path: 'scroll', component: ScrollingComponent },
    { path: 'llm', component: LLMComponent },
    { path: 'pics', component: PictureComponent },
    { path: ':dynamicValue', component: PropertyFormComponent },   
];
