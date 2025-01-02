import { Component } from '@angular/core';
import { versionInfo } from './version-info';
import { RouterModule } from '@angular/router';

@Component({
    selector: 'app-root',
    imports: [RouterModule],
    templateUrl: './app.component.html',
    styleUrls: ['./app.component.scss'],
    
})
export class AppComponent {
  title = 'NewDjangoSite';
  gitVersion: string = versionInfo.hash;
}
