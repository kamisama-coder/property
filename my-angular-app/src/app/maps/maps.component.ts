import { Component, Inject, PLATFORM_ID, OnInit, AfterViewInit } from '@angular/core';
import { isPlatformBrowser } from '@angular/common';
import { HttpClient } from '@angular/common/http';
import { ActivatedRoute } from '@angular/router';
import { ReactiveFormsModule, FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { HttpClientModule } from '@angular/common/http';


@Component({
  selector: 'app-maps',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, FormsModule, HttpClientModule],
  templateUrl: './maps.component.html',
  styleUrl: './maps.component.css'
})
export class MapsComponent implements OnInit, AfterViewInit {
  private map: any;
  private markerGroup: any;
  public queryValue: string = '';
  private lat: number = 0;
  private lon: number = 0;
  private L: any; // ✅ Leaflet as a class property

  constructor(
    private http: HttpClient,
    private route: ActivatedRoute,
    @Inject(PLATFORM_ID) private platformId: Object
  ) {}

  ngOnInit() {
    this.route.queryParams.subscribe(params => {
      this.lat = params['latt'];
      this.lon = params['long'];
    });
  }

  async ngAfterViewInit(): Promise<void> {
    if (isPlatformBrowser(this.platformId)) {
      
      this.L = await import('leaflet');
      this.L.Icon.Default.mergeOptions({
      iconUrl: 'assets/meow.png',
      iconRetinaUrl: 'assets/meow.png', 
      shadowUrl: '' 
      });

      this.map = this.L.map('map').setView([this.lat, this.lon], 13);

      this.L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; OpenStreetMap contributors'
      }).addTo(this.map);

      this.markerGroup = this.L.layerGroup().addTo(this.map);
      this.L.marker([this.lat, this.lon])
      .addTo(this.markerGroup)
      .bindPopup('Initial Location')
      .openPopup();
    }
  }

  searchLocation(): void {
    this.markerGroup.clearLayers();

    this.L.marker([this.lat, this.lon])
      .addTo(this.markerGroup)
      .bindPopup('Initial Location')
      .openPopup();

    const query = {
      lat: this.lat,
      lon: this.lon,
      value: this.queryValue
    };

    this.http.post<any>('http://127.0.0.1:5000/system_design', query).subscribe({
      next: (response) => {
        console.log(response)
        const storage = response;

        for (let i = 0; i < storage.length; i++) {
          var lat = storage[i].latitude;
          var lon = storage[i].longitude;
          var place = storage[i].name;
          console.log(lat);
          this.L.marker([lat, lon])
            .addTo(this.markerGroup)
            .bindPopup(`Location: ${lat}, ${lon}<br>Place: ${place}`);
        }
      },
      error: () => {
        console.error("AJAX error occurred.");
      }
    });
  }
}
