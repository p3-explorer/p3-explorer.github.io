
var searchType = 0 
function changeSearch(i){
  searchType = i;
  if(i == 1){
    document.getElementsByName("search")[0].placeholder = 'Search for Categories...';
  }else{
    document.getElementsByName("search")[0].placeholder = 'Search for Apps...';
  }
}
function mySearch() {
  var input, filter, table, tr, td, i, txtValue;
  input = document.getElementById("myInput");
  filter = input.value.toUpperCase();
  table = document.getElementById("myTable");
  tr = table.getElementsByTagName("tr");
  for (i = 0; i < tr.length; i++) {
    td = tr[i].getElementsByTagName("td")[searchType];
    if (td) {
      txtValue = td.textContent || td.innerText;
      if (txtValue.toUpperCase().indexOf(filter) > -1) {
        tr[i].style.display = "";
      } else {
        tr[i].style.display = "none";
      }
    }       
  }
}
