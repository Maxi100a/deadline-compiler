function compile() {
  // Change this
  var calendar_url = "";

  var response = UrlFetchApp.fetch(calendar_url).getContentText().split("\n");

  var events = [];
  
  // Load all events into an array
  var current = []
  for (var i = 0; i < response.length; i++){
    var line = response[i];
    if (line.indexOf('DTSTART') > -1 && current.length == 0){
      var undate = line.split(":")[1].substr(0, 8);
      var year = undate.substring(0,4);
      var month = undate.substring(4,6);
      var day = undate.substring(6);
      var date = '=DATEVALUE("' + month + "/" + day + "/" + year + '")';
      current.push(date);
    }

    if(line.indexOf('SUMMARY:') > -1 && current.length == 1){
      var event_name = line.split(":");
      event_name.shift() // remove SUMMARY
      while (response[i + 1].startsWith(" ")){
        var last_index = event_name.length - 1;
        event_name[last_index] = event_name[last_index].slice(0, -1);
        event_name[last_index] += response[i + 1].substring(1);
        i++;
      }

      current.push(event_name.join(":"));
      events.push(current);
      current = [];
    }

  }

  var sheet = SpreadsheetApp.getActiveSheet();
  var rules = [];
  var checkbox = SpreadsheetApp.newDataValidation().requireCheckbox().build();
  var header_values = [
    ['Date Due', 'Assignment', 'Completed']
  ];

  var header = sheet.getRange("A1:C1");
  var cells = sheet.getRange("A2:B" + (events.length + 1));
  var full_cells = sheet.getRange("A2:C" + (events.length + 1));

  var conditional_false = SpreadsheetApp.newConditionalFormatRule().whenFormulaSatisfied("=$C2=FALSE").setRanges([full_cells]).setBackground("#f4c7c3");
  var conditional_true = SpreadsheetApp.newConditionalFormatRule().whenFormulaSatisfied("=$C2=TRUE").setRanges([full_cells]).setBackground("#b7e1cd");
  sheet.getRange('C2:C' + (events.length + 1)).setDataValidation(checkbox);

  
  rules.push(conditional_false);
  rules.push(conditional_true);
  sheet.setConditionalFormatRules(rules);

  cells.setValues(events);
  full_cells.setFontSize(13);
  header.setValues(header_values);
  header.setFontSize(14);
  header.setBackground("#bababa");
  header.setFontWeight("bold");
}
