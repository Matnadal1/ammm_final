int N = ...;
int D = ...;

//input
range NN = 1..N;
range DD = 1..D;

float d[i in NN] = ...;
float n[p in DD] = ...;
float m[i in NN, j in NN] = ...;


//auxiliary indices
dvar boolean x[i in NN];
dvar boolean x_ij[i in NN, j in NN];
dvar boolean y_ip[i in NN, p in DD];

//objective function
dvar float+ z;

execute{
}


// Objective
maximize z;

subject to{
  
  Constraint1:
  // y_ip is setted to one only when member i belongs to department p
  forall(i in NN)
    forall(p in DD)
  	y_ip[i, p] == (d[i] == p);
  	
  Constraint2:
  // x_ij is setted to one only when both members i and j belong to the committee
  forall(i in NN, j in NN){ 
 	 x_ij[i,j] <= x[i];
  	 x_ij[i,j] <= x[j];
 	 x_ij[i,j] >= x[i] + x[j] - 1;
   } 
  
  Contraint3:
  // The sum number of members in the committee must be equal to the total numbers of members that represents every department.
  sum(i in NN) x[i] == sum(p in DD) n[p];
    
  Contraint4:
  // Each department must have n_p representatives in the committee.
  forall(p in DD)
    sum(i in NN) y_ip[i, p] * x[i] >= n[p];
    
  Contraint5:
  // If two members are incompatible, at most 1 of them can be in the commission.
  forall(i in NN)
    forall(j in NN)
	  if (i < j) 
	    if (m[i, j] == 0) x_ij[i,j] == 0;
    		
  Constraint6:
  // If two members get along poorly there must be a third one that goes along well with both of them
  forall(i in NN)
    forall(j in NN)
    if(i < j)
      if(m[i, j] < 0.15)
        sum(k in NN: k != i && k != j) 
          (x[k] * ((m[i, k] >= 0.851) && (m[j, k] >= 0.851))) >= x_ij[i,j];
  
  ConstraintZ:
  // Sum of the compatibility between members.
  z <= sum(i in NN) sum(j in NN: i<j) m[i, j] * x_ij[i, j];
}


execute {
  var count=0;
  var div=0;
  var ob=0.0;
  
  write("members of the commission:")
  for(var i=1; i<=N; i++){
    if(x[i]==1){
     	write(i+" ");
     	count++;
     }
   }   
  writeln();
   
   div = count * (count - 1) / 2;
  
  if(div>0){
    ob=z/div;
  }
   write("objective:"+ ob);
}