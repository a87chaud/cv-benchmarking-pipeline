import { Component, EventEmitter, Input, Output } from '@angular/core';

export interface ButtonGroupConfig {
  text: string,
  value: string
}
@Component({
  selector: 'app-button-group-component',
  imports: [],
  templateUrl: './button-group-component.html',
  styleUrl: './button-group-component.css',
  standalone: true
})
export class ButtonGroupComponent {
  @Input() buttonConfigs!: ButtonGroupConfig[];
  @Output() outputButton = new EventEmitter<string>();

  selectButton(val: string): void {
    this.outputButton.emit(val)
  }
}
