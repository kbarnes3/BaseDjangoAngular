import { Component, ChangeDetectionStrategy } from '@angular/core';
import { versionInfo } from './version-info';
import { RouterModule } from '@angular/router';
import { NavBarComponent } from './nav-bar/nav-bar.component';

@Component({
    selector: 'app-root',
    imports: [RouterModule, NavBarComponent],
    templateUrl: './app.component.html',
    changeDetection: ChangeDetectionStrategy.OnPush,
    styleUrls: ['./app.component.scss'],
    
})
export class AppComponent {
  title = 'NewDjangoSite';
  gitVersion: string = versionInfo.hash;
}
