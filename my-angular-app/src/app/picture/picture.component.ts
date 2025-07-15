import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpClient } from '@angular/common/http';
import { HttpClientModule } from '@angular/common/http';
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-picture',
  imports: [CommonModule,FormsModule,HttpClientModule],
  templateUrl: './picture.component.html',
  styleUrl: './picture.component.css'
})
export class PictureComponent {

  picture:any[] = []
  index:number = 0;

  constructor(private route: ActivatedRoute, private http: HttpClient,){

  }

  ngOnInit() {
  this.route.queryParams.subscribe(params => {
    this.index = params['index'];

    this.http.get<any>('http://127.0.0.1:5000/pics', {
      params: { index: this.index }
    }).subscribe({
      next: (response) => {
        if(response.length == 0){alert("No image avalaible")}
        else{ this.picture = response}
      }
    });
  });
}
}
