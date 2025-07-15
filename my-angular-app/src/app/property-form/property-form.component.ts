// property-form.component.ts
import { Component, inject, OnDestroy } from '@angular/core';
import { FormBuilder, FormGroup, FormsModule, ReactiveFormsModule , Validators} from '@angular/forms';
import { CommonModule } from '@angular/common';
import { HttpClient } from '@angular/common/http';
import { debounceTime, switchMap, of, Subscription } from 'rxjs';
import { ActivatedRoute } from '@angular/router';
import { HttpClientModule } from '@angular/common/http';


@Component({
  selector: 'app-property-form',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, HttpClientModule, FormsModule],
  templateUrl: './property-form.component.html',
  styleUrls: ['./property-form.component.css']
})
export class PropertyFormComponent implements OnDestroy {
  fb = inject(FormBuilder);
  http = inject(HttpClient);
  route = inject(ActivatedRoute)

 propertyForm: FormGroup = this.fb.group({
  address: ['', Validators.required],
  size: [1, Validators.required],
  price_suffix: ['Lakh', Validators.required],
  price: [100000, Validators.required],
  area_sqft: [13, Validators.required],
  status: ['Rent', Validators.required],
  proxy_address: ['', Validators.required],
  long: ['', Validators.required],
  latt: ['', Validators.required],
  id: ['', Validators.required],
  phone: ['', Validators.required]
});

  editing = false;
  suggestions: any[] = [];
  editid = '';
  imageInputs: { vector: string, files: FileList | null }[] = [];
  inputvalue = 0;
  kami = 3;
  addressSub: Subscription | undefined;
  cover : { vector: string, files: FileList | null } = { vector: 'cover', files: null };

  

  constructor() {
   this.route.queryParams.subscribe(params => {
      this.editing = params['edit'] || false;
      this.editid = params['index']
    }); 
   if (this.editing) {
    this.http.get<any>('http://localhost:5000/edit/'+this.editid).subscribe({
      next: (response) => {
        const post = response[0]; // adjust if your API structure changes

        this.propertyForm.patchValue({
          address: post.address,
          size: post.size,
          price_suffix: post.price_suffix,
          price: post.price,
          area_sqft: post.area_sqft,
          status: post.status,
          proxy_address: post.proxy_address,
          long: post.long,
          latt: post.latt,
          id: post.user_id,
          phone: post.phone
        });
        for(let i=0;i<response[0].pics.length;i++){
          this.addImageQuery(response[0].pics[i])

        }
      },
      error: (err) => {
        console.error('Error fetching post data:', err);
      }
    });
  }  

  this.addressSub = this.propertyForm.get('proxy_address')!.valueChanges
    .pipe(
      debounceTime(300),
      switchMap((input: string) => {
        if (input && input.length > this.kami) {
          return this.fetchSuggestions(input); 
        } else {
          this.suggestions = [];
          return of([]); 
        }
      })
    )
    .subscribe(data => {
      if (!data.length) {
        this.suggestions = [
          {
            display_name: 'No results found. Try a different query.',
            lat: '',
            lon: '',
            isError: true
          }
        ];
      } else {
        this.suggestions = data;
      }
    });
}

  ngOnInit() {
    this.route.paramMap.subscribe(params => {
      this.propertyForm.patchValue({ id: params.get('dynamicValue') });
    });
  }


  fetchSuggestions(input: string) {
    const params = new URLSearchParams({
      q: input.replace(/ /g, '+'),
      format: 'json',
      addressdetails: '1',
      polygon_geojson: '0'
    });
    const url = `https://nominatim.openstreetmap.org/search?${params.toString()}`;
    return this.http.get<any[]>(url);
  }


  onFileSelected(suggestion: any) {
    if (suggestion.isError) return;

    this.propertyForm.patchValue({
      proxy_address: suggestion.display_name,
      long: suggestion.lon,
      latt: suggestion.lat
    });
    this.suggestions = [];
  }

  onSubmit() {
    if (this.propertyForm.valid) {
      console.log('Form submitted:', this.propertyForm.value);
    } else {
      console.error('Form is invalid');
    }
  }

  handlecoverinpput(event: any) {
   this.cover.files = event.target.files;
}

  addImageQuery(value:string|null) {
    this.imageInputs.push({ vector: value || '', files: null });
    this.inputvalue++;
  }

  handleFileInput(event: any, index: number) {
    this.imageInputs[index].files = event.target.files;
  }

  submitForm() {
  const formData = new FormData();

  // ✅ Append JSON form data
  if (this.propertyForm.valid) {
    const jsonData = this.propertyForm.value;
    formData.append('form', JSON.stringify(jsonData));
  } else {
    alert('Please fill out the form correctly');
    return;
  }

  // ✅ Append additional images
  this.imageInputs.forEach(input => {
    if (input.vector && input.files) {
      Array.from(input.files).forEach(file => {
        formData.append(`${input.vector}[]`, file);
      });
    }
  });

  // ✅ Append cover photo
  if (this.cover.vector && this.cover.files) {
    Array.from(this.cover.files).forEach(file => {
      formData.append(`${this.cover.vector}[]`, file);
    });
  }

  // ✅ Submit the form
  if(this.editing == false){
    this.http.post('http://127.0.0.1:5000/', formData).subscribe({
    next: (res) => console.log('Upload successful:', res),
    error: (err) => console.error('Upload error:', err)
  });
  }
  else{
    this.http.post('http://127.0.0.1:5000/edit/'+this.editid, formData).subscribe({
    next: (res) => console.log('Upload successful:', res),
    error: (err) => console.error('Upload error:', err)
  });
  }
  
}

  ngOnDestroy() {
    this.addressSub?.unsubscribe();
  }
}
