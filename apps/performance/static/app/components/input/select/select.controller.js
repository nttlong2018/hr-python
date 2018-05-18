(function () {
  'use strict';

  angular.module('ZebraApp.components.inputs')
    .controller('SelectpickerPanelCtrl', SelectpickerPanelCtrl);

  /** @ngInject */
  function SelectpickerPanelCtrl($scope, $sce) {

    var vm = this;
    vm.disabled = undefined;


    vm.standardItem = {};
    vm.standardSelectItems = [
      {label: $sce.trustAsHtml('Option 1'), value: 1},
      {label: $sce.trustAsHtml('Option 2'), value: 2},
      {label: $sce.trustAsHtml('Option 3'), value: 3},
      {label: $sce.trustAsHtml('Option 4'), value: 4}
    ];

    vm.withSearchItem = {};

    vm.selectWithSearchItems = [
      {label: $sce.trustAsHtml('Hot Dog, Fries and a Soda'), value: 1},
      {label: $sce.trustAsHtml('Burger, Shake and a Smile'), value: 2},
      {label: $sce.trustAsHtml('Sugar, Spice and all things nice'), value: 3},
      {label: $sce.trustAsHtml('Baby Back Ribs'), value: 4}
    ];
    vm.groupedItem = {};
    vm.groupedSelectItems = [
      {label: $sce.trustAsHtml('Group 1 - Option 1'), value: 1, group: 'Group 1'},
      {label: $sce.trustAsHtml('Group 2 - Option 2'), value: 2, group: 'Group 2'},
      {label: $sce.trustAsHtml('Group 1 - Option 3'), value: 3, group: 'Group 1'},
      {label: $sce.trustAsHtml('Group 2 - Option 4'), value: 4, group: 'Group 2'}
    ];

    vm.groupedByItem = {};
    vm.groupedBySelectItems = [
      {name: $sce.trustAsHtml('Adam'), country: $sce.trustAsHtml('United States')},
      {name: $sce.trustAsHtml('Amalie'), country: $sce.trustAsHtml('Argentina')},
      {name: $sce.trustAsHtml('Estefanía'), country: $sce.trustAsHtml('Argentina')},
      {name: $sce.trustAsHtml('Adrian'), country: $sce.trustAsHtml('Ecuador')},
      {name: $sce.trustAsHtml('Wladimir'), country: $sce.trustAsHtml('Ecuador')},
      {name: $sce.trustAsHtml('Samantha'), country: $sce.trustAsHtml('United States')},
      {name: $sce.trustAsHtml('Nicole'), country: $sce.trustAsHtml('Colombia')},
      {name: $sce.trustAsHtml('Natasha'), country: $sce.trustAsHtml('Ecuador')},
      {name: $sce.trustAsHtml('Michael'), country: $sce.trustAsHtml('Colombia')},
      {name: $sce.trustAsHtml('Nicolás'), country: $sce.trustAsHtml('Colombia')}
    ];
    vm.someGroupFn = function (item) {

      if (item.name[0] >= 'A' && item.name[0] <= 'M')
        return 'From A - M';
      if (item.name[0] >= 'N' && item.name[0] <= 'Z')
        return 'From N - Z';
    };

    vm.disableItem = {};
    vm.disableItems = [];

    vm.multipleItem = {};
    vm.multipleSelectItems = [
      {label: $sce.trustAsHtml('Option 1'), value: 1},
      {label: $sce.trustAsHtml('Option 2'), value: 2},
      {label: $sce.trustAsHtml('Option 3'), value: 3},
      {label: $sce.trustAsHtml('Option 4'), value: 4},
      {label: $sce.trustAsHtml('Option 5'), value: 5},
      {label: $sce.trustAsHtml('Option 6'), value: 6},
      {label: $sce.trustAsHtml('Option 7'), value: 7},
      {label: $sce.trustAsHtml('Option 8'), value: 8}
    ];
    vm.withDeleteItem = {};
    vm.withDeleteSelectItems = [
      {label: $sce.trustAsHtml('Option 1'), value: 1},
      {label: $sce.trustAsHtml('Option 2'), value: 2},
      {label: $sce.trustAsHtml('Option 3'), value: 3},
      {label: $sce.trustAsHtml('Option 4'), value: 4},
      {label: $sce.trustAsHtml('Option 5'), value: 5},
      {label: $sce.trustAsHtml('Option 6'), value: 6},
      {label: $sce.trustAsHtml('Option 7'), value: 7},
      {label: $sce.trustAsHtml('Option 8'), value: 8}
    ];

  }
})();
