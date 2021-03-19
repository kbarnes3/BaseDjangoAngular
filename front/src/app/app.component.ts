import { Component } from '@angular/core';
import { versionInfo } from './version-info';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {
  title = 'NewDjangoSite';
  gitVersion: string = versionInfo.hash;
}
