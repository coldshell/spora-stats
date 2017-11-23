#!/usr/bin/octave 
# Package
pkg load optim

# Get args
arg_list = argv();
argc = size(arg_list,1);
csv_file = arg_list{1};

# Get Delim
if (argc == 2)
    delim = arg_list{2};
else
    delim = ';';
endif

# Retrive CSV informations
csv = dlmread(csv_file, delim);
price = csv(2:end, 10);
# Get the right category column
for i = 4:9
    if (csv(4, i) != 0)
        nb_enc_files = csv(2:end, i);
    endif
endfor
#
# Linear regression
#
sz =size(nb_enc_files, 1);
F = [ones(sz, 1), nb_enc_files(:)];
[p,e_var,r,p_var,y_var] = LinearRegression(F,price);
estimation = F*p;

#
# Plotting
#
f = figure;

plot(nb_enc_files, price);
hold on;
plot(nb_enc_files, price, 'b..');
plot(nb_enc_files, estimation, 'g--');
plot(nb_enc_files, round(estimation), 'r..');
xlabel("Number of encrypted files");
ylabel("Price");
legend("Category", "Sample", "Estimation", "Rounded estimation");

waitfor(f);

#
# Report
#
printf("Equation  %d * x + %d", p(2), p(1));
