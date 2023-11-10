table = readtable('openmic-2018-aggregated-labels.csv', 'ReadRowNames', true);

Instrument = 'trumpet';

% Filter rows with 'trumpet' label
trumpetRows = table(strcmp(table.instrument, 'trumpet'), :);

% Extract sample keys and labels for trumpet
trumpetSampleKeys = trumpetRows.sample_key;
trumpetLabels = trumpetRows.instrument;

% [audioIn,fs]=audioread("000135_483840.ogg");
% 
% aFE = audioFeatureExtractor( ...
%     SampleRate=fs, ...
%     Window=hamming(round(0.03*fs),"periodic"), ...
%     OverlapLength=round(0.02*fs), ...
%     mfcc=true, ...
%     mfccDelta=true, ...
%     mfccDeltaDelta=true, ...
%     pitch=true, ...
%     spectralCentroid=true, ...
%     zerocrossrate=true, ...
%     shortTimeEnergy=true);
% 
% features = extract(aFE, audioIn);
% 
